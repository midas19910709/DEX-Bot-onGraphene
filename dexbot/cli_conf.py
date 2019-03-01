"""
A module to provide an interactive text-based tool for dexbot configuration
The result is dexbot can be run without having to hand-edit config files.
If systemd is detected it will offer to install a user service unit (under ~/.local/share/systemd)
This requires a per-user systemd process to be running

Requires the 'whiptail' tool for text-based configuration (so UNIX only)
if not available, falls back to a line-based configurator ("NoWhiptail")

Note there is some common cross-UI configuration stuff: look in base.py
It's expected GUI/web interfaces will be re-implementing code in this file, but they should
understand the common code so worker strategy writers can define their configuration once
for each strategy class.
"""

import importlib
import pathlib
import os
import os.path
import sys
import re
import subprocess

from dexbot.whiptail import get_whiptail
from dexbot.strategies.base import StrategyBase
import dexbot.helper

STRATEGIES = [
    {'tag': 'relative',
     'class': 'dexbot.strategies.relative_orders',
     'name': 'Relative Orders'},
    {'tag': 'stagger',
     'class': 'dexbot.strategies.staggered_orders',
     'name': 'Staggered Orders'}]

tags_so_far = {'stagger', 'relative'}
for desc, module in dexbot.helper.find_external_strategies():
    tag = desc.split()[0].lower()
    # make sure tag is unique
    i = 1
    while tag in tags_so_far:
        tag = tag+str(i)
        i += 1
    tags_so_far.add(tag)
    STRATEGIES.append({'tag': tag, 'class': module, 'name': desc})

SYSTEMD_SERVICE_NAME = os.path.expanduser(
    "~/.local/share/systemd/user/dexbot.service")

SYSTEMD_SERVICE_FILE = """
[Unit]
Description=Dexbot

[Service]
Type=notify
WorkingDirectory={homedir}
ExecStart={exe} --systemd run
TimeoutSec=20m
Environment=PYTHONUNBUFFERED=true
Environment=UNLOCK={passwd}

[Install]
WantedBy=default.target
"""


def select_choice(current, choices):
    """ For the radiolist, get us a list with the current value selected """
    return [(tag, text, (current == tag and "ON") or "OFF")
            for tag, text in choices]


def process_config_element(elem, whiptail, config):
    """ Process an item of configuration metadata display a widget as appropriate
        d: the Dialog object
        config: the config dictionary for this worker
    """
    if elem.description:
        title = '{} - {}'.format(elem.title, elem.description)
    else:
        title = elem.title

    if elem.type == "string":
        txt = whiptail.prompt(title, config.get(elem.key, elem.default))
        if elem.extra:
            while not re.match(elem.extra, txt):
                whiptail.alert("The value is not valid")
                txt = whiptail.prompt(
                    title, config.get(
                        elem.key, elem.default))
        config[elem.key] = txt

    if elem.type == "bool":
        value = config.get(elem.key, elem.default)
        value = 'yes' if value else 'no'
        config[elem.key] = whiptail.confirm(title, value)

    if elem.type in ("float", "int"):
        while True:
            if elem.type == 'int':
                template = '{}'
            else:
                template = '{:.8f}'
            txt = whiptail.prompt(title, template.format(config.get(elem.key, elem.default)))
            try:
                if elem.type == "int":
                    val = int(txt)
                else:
                    val = float(txt)
                if val < elem.extra[0]:
                    whiptail.alert("The value is too low")
                elif elem.extra[1] and val > elem.extra[1]:
                    whiptail.alert("the value is too high")
                else:
                    break
            except ValueError:
                whiptail.alert("Not a valid value")
        config[elem.key] = val

    if elem.type == "choice":
        config[elem.key] = whiptail.radiolist(title, select_choice(
            config.get(elem.key, elem.default), elem.extra))


def dexbot_service_running():
    """ Return True if dexbot service is running
    """
    cmd = 'systemctl --user status dexbot'
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in output.stdout.readlines():
        if b'Active:' in line and b'(running)' in line:
            return True
    return False


def setup_systemd(whiptail, config):
    if not os.path.exists("/etc/systemd"):
        return  # No working systemd

    if not whiptail.confirm(
            "Do you want to run dexbot as a background (daemon) process?"):
        config['systemd_status'] = 'disabled'
        return

    redo_setup = False
    if os.path.exists(SYSTEMD_SERVICE_NAME):
        redo_setup = whiptail.confirm('Redo systemd setup?', 'no')

    if not os.path.exists(SYSTEMD_SERVICE_NAME) or redo_setup:
        path = '~/.local/share/systemd/user'
        path = os.path.expanduser(path)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        password = whiptail.prompt(
            "The uptick wallet password\n"
            "NOTE: this will be saved on disc so the worker can run unattended. "
            "This means anyone with access to this computer's files can spend all your money",
            password=True)

        # Because we hold password be restrictive
        fd = os.open(SYSTEMD_SERVICE_NAME, os.O_WRONLY | os.O_CREAT, 0o600)
        with open(fd, "w") as fp:
            fp.write(
                SYSTEMD_SERVICE_FILE.format(
                    exe=sys.argv[0],
                    passwd=password,
                    homedir=os.path.expanduser("~")))
        # The dexbot service file was edited, reload the daemon configs
        os.system('systemctl --user daemon-reload')

    # Signal cli.py to set the unit up after writing config file
    config['systemd_status'] = 'enabled'


def get_strategy_tag(strategy_class):
    for strategy in STRATEGIES:
        if strategy_class == strategy['class']:
            return strategy['tag']
    return None


def configure_worker(whiptail, worker_config):
    # By default always editing
    editing = True

    if not worker_config:
        editing = False

    default_strategy = worker_config.get('module', 'dexbot.strategies.relative_orders')
    strategy_list = []

    for strategy in STRATEGIES:
        if default_strategy == strategy['class']:
            default_strategy = strategy['tag']

        # Add strategy tag and name pairs to a list
        strategy_list.append([strategy['tag'], strategy['name']])

    # Strategy selection
    worker_config['module'] = whiptail.radiolist(
        "Choose a worker strategy",
        select_choice(default_strategy, strategy_list)
    )

    for strategy in STRATEGIES:
        if strategy['tag'] == worker_config['module']:
            worker_config['module'] = strategy['class']

    # Import the strategy class but we don't __init__ it here
    strategy_class = getattr(
        importlib.import_module(worker_config["module"]),
        'Strategy'
    )

    # Check if strategy has changed and editing existing worker
    if editing and default_strategy != get_strategy_tag(worker_config['module']):
        new_worker_config = {}

        # If strategy has changed, create new config where base elements stay the same
        for config_item in StrategyBase.configure():
            try:
                key = config_item[0]
                new_worker_config[key] = worker_config[key]
            except KeyError as error:
                # In case using old configuration file and there are new fields, this passes missing key
                pass

        # Add module separately to the config
        new_worker_config['module'] = worker_config['module']
        worker_config = new_worker_config

    # Use class metadata for per-worker configuration
    config_elems = strategy_class.configure()
    if config_elems:
        # Strategy options
        for elem in config_elems:
            process_config_element(elem, whiptail, worker_config)
    else:
        whiptail.alert(
            "This worker type does not have configuration information. "
            "You will have to check the worker code and add configuration values to config.yml if required")
    return worker_config


def configure_dexbot(config, ctx):
    whiptail = get_whiptail('DEXBot configure')
    workers = config.get('workers', {})
    if not workers:
        while True:
            txt = whiptail.prompt("Your name for the worker")
            config['workers'] = {txt: configure_worker(whiptail, {})}
            if not whiptail.confirm("Set up another worker?\n(DEXBot can run multiple workers in one instance)"):
                break
        setup_systemd(whiptail, config)
    else:
        bitshares_instance = ctx.bitshares
        action = whiptail.menu(
            "You have an existing configuration.\nSelect an action:",
            [('NEW', 'Create a new worker'),
             ('DEL', 'Delete a worker'),
             ('EDIT', 'Edit a worker'),
             ('CONF', 'Redo general config')])

        if action == 'EDIT':
            worker_name = whiptail.menu("Select worker to edit", [(index, index) for index in workers])
            config['workers'][worker_name] = configure_worker(whiptail, config['workers'][worker_name])

            strategy = StrategyBase(worker_name, bitshares_instance=bitshares_instance, config=config)
            strategy.clear_all_worker_data()
        elif action == 'DEL':
            worker_name = whiptail.menu("Select worker to delete", [(index, index) for index in workers])
            del config['workers'][worker_name]

            strategy = StrategyBase(worker_name, bitshares_instance=bitshares_instance, config=config)
            strategy.clear_all_worker_data()
        elif action == 'NEW':
            txt = whiptail.prompt("Your name for the new worker")
            config['workers'][txt] = configure_worker(whiptail, {})
        elif action == 'CONF':
            choice = whiptail.node_radiolist(
                msg="Choose node",
                items=select_choice(config['node'][0], [(index, index) for index in config['node']])
            )
            # Move selected node as first item in the config file's node list
            config['node'].remove(choice)
            config['node'].insert(0, choice)

            setup_systemd(whiptail, config)
    whiptail.clear()
    return config
