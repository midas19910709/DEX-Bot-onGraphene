import os
import sys
import click
import logging
import logging.config
from ruamel import yaml
from functools import update_wrapper
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
log = logging.getLogger(__name__)


def verbose(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        verbosity = [
            "critical", "error", "warn", "info", "debug"
        ][int(min(ctx.obj.get("verbose", 0), 4))]
        if ctx.obj.get("systemd", False):
            # Don't print the timestamps: systemd will log it for us
            formatter1 = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            formatter2 = logging.Formatter(
                'bot %(botname)s using account %(account)s on %(market)s - %(levelname)s - %(message)s'
            )
        elif verbosity == "debug":
            # When debugging log where the log call came from
            formatter1 = logging.Formatter(
                '%(asctime)s (%(module)s:%(lineno)d) - %(levelname)s - %(message)s'
            )
            formatter2 = logging.Formatter(
                '%(asctime)s (%(module)s:%(lineno)d) - bot %(botname)s - %(levelname)s - %(message)s'
            )
        else:
            formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter2 = logging.Formatter(
                '%(asctime)s - bot %(botname)s using account %(account)s on %(market)s - %(levelname)s - %(message)s'
            )

        # Use special format for special bots logger
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, verbosity.upper()))
        ch.setFormatter(formatter2)
        logging.getLogger("dexbot.per_bot").addHandler(ch)
        logging.getLogger("dexbot.per_bot").propagate = False  # Don't double up with root logger
        # Set the root logger with basic format
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, verbosity.upper()))
        ch.setFormatter(formatter1)
        logging.getLogger("dexbot").addHandler(ch)
        logging.getLogger("").handlers = []
        
        # GrapheneAPI logging
        if ctx.obj["verbose"] > 4:
            verbosity = [
                "critical", "error", "warn", "info", "debug"
            ][int(min(ctx.obj.get("verbose", 4) - 4, 4))]
            log = logging.getLogger("grapheneapi")
            log.setLevel(getattr(logging, verbosity.upper()))
            log.addHandler(ch)
        if ctx.obj["verbose"] > 8:
            verbosity = [
                "critical", "error", "warn", "info", "debug"
            ][int(min(ctx.obj.get("verbose", 8) - 8, 4))]
            log = logging.getLogger("graphenebase")
            log.setLevel(getattr(logging, verbosity.upper()))
            log.addHandler(ch)
        # has the user set logging in the config
        if "logging" in ctx.config:
            # this is defined in https://docs.python.org/3.4/library/logging.config.html#logging-config-dictschema
            logging.config.dictConfig(ctx.config['logging'])
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def chain(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        ctx.bitshares = BitShares(
            ctx.config["node"],
            **ctx.obj
        )
        set_shared_bitshares_instance(ctx.bitshares)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def unlock(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if not ctx.obj.get("unsigned", False):
            systemd = ctx.obj.get('systemd', False)
            if ctx.bitshares.wallet.created():
                if "UNLOCK" in os.environ:
                    pwd = os.environ["UNLOCK"]
                else:
                    if systemd:
                        # No user available to interact with
                        log.critical("Passphrase not available, exiting")
                        sys.exit(78)  # 'configuration error' in sysexits.h
                    pwd = click.prompt(
                        "Current Wallet Passphrase", hide_input=True)
                ctx.bitshares.wallet.unlock(pwd)
            else:
                if systemd:
                    # No user available to interact with
                    log.critical("Wallet not installed, cannot run")
                    sys.exit(78)
                click.echo("No wallet installed yet. Creating ...")
                pwd = click.prompt(
                    "Wallet Encryption Passphrase",
                    hide_input=True,
                    confirmation_prompt=True)
                ctx.bitshares.wallet.create(pwd)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def configfile(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        try:
            ctx.config = yaml.safe_load(open(ctx.obj["configfile"]))
        except FileNotFoundError:
            alert("Looking for the config file in %s\nNot found!\n"
                  "Try running 'dexbot configure' to generate\n" % ctx.obj['configfile'])
            sys.exit(78)  # 'configuration error' in sysexits.h
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def priceChange(new, old):
    if float(old) == 0.0:
        return -1
    else:
        percent = ((float(new) - float(old))) / float(old) * 100
        if percent >= 0:
            return click.style("%.2f" % percent, fg="green")
        else:
            return click.style("%.2f" % percent, fg="red")


def formatPrice(f):
    return click.style("%.10f" % f, fg="yellow")


def formatStd(f):
    return click.style("%.2f" % f, bold=True)


def warning(msg):
    click.echo(
        "[" +
        click.style("Warning", fg="yellow") +
        "] " + msg
    )


def confirmwarning(msg):
    return click.confirm(
        "[" +
        click.style("Warning", fg="yellow") +
        "] " + msg
    )


def alert(msg):
    click.echo(
        "[" +
        click.style("Alert", fg="red") +
        "] " + msg
    )


def confirmalert(msg):
    return click.confirm(
        "[" +
        click.style("Alert", fg="red") +
        "] " + msg
    )
