#!/usr/bin/env python
# Copyright 2019 XOE Labs (<https://xoe.solutions>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

__version__ = "0.1.1"

import sys

import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

CONTEXT_SETTINGS = dict(auto_envvar_prefix="ODOOUP")


@with_plugins(iter_entry_points("core_package.cli_plugins"))
@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Commandline interface for OdooUp commands."""
    pass


@main.command()
def version():
    """Show the OdooUp version."""
    click.secho("Click Version: {}".format(click.__version__), fg="green")
    click.secho("Python Version: {}".format(sys.version), fg="green")
    click.secho("OdooUp Version: {}".format(__version__), fg="yellow")
