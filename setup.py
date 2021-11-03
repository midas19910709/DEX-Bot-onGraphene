#!/usr/bin/env python3
from distutils.command import build as build_module

from setuptools import find_packages, setup

from dexbot import APP_NAME, VERSION

cmd_class = {}
console_scripts = ['dexbot-cli = dexbot.cli:main']
install_requires = []


class BuildCommand(build_module.build):
    def run(self):
        self.run_command('build_ui')
        build_module.build.run(self)


try:
    from pyqt_distutils.build_ui import build_ui

    cmd_class = {'build_ui': build_ui, 'build': BuildCommand}
    console_scripts.append('dexbot-gui = dexbot.gui:main')
    install_requires.extend(["pyqt-distutils"])
except BaseException as e:
    print("GUI not available: {}".format(e))


setup(
    name=APP_NAME,
    version=VERSION,
    description='Trading bot for the DEX (Graphene)',
    long_description=open('README.md').read(),
    author='Codaone Oy',
    author_email='support@codaone.com',
    maintainer='Codaone Oy',
    maintainer_email='support@codaone.com',
    url='https://github.com/graphene-blockchain/DEXBot',
    keywords=['DEX', 'bot', 'trading', 'api', 'blockchain', "graphene"],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    cmdclass=cmd_class,
    entry_points={'console_scripts': console_scripts},
    install_requires=[
        "pyqt5==5.10",
        "pyqt-distutils==0.7.3",
        "pyinstaller==3.4",
        "click-datetime==0.2",
        "aiohttp==3.7.4",
        "requests==2.22.0",
        "yarl==1.6.3",
        "ccxt==1.58.17",
        "pywaves==0.8.20",
        "graphenelib==1.2.0",
        "bitshares",
        "uptick==0.2.4",
        "ruamel.yaml>=0.15.37",
        "appdirs==1.4.3",
        "pycryptodomex==3.6.4",
        "websocket-client==0.56.0",
        "sdnotify==0.3.2",
        "sqlalchemy==1.3.0",
        "click==7.0",
        "alembic==1.0.11",
    ],
    dependency_links=[
        'git+git://github.com/graphene-blockchain/python-bitshares@for_dexbot#egg=bitshares'
    ],
    include_package_data=True,
)
