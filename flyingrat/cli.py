# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

import os
import asyncore
from smtpd import SMTPServer
import tempfile

import click

from .store import Store
from .pop3 import Server as Pop3Server


def parse_address(address):
    parts = address.split(':')
    return ':'.join(parts[:-1]), int(parts[-1])


def validate_address(ctx, param, value):
    try:
        return parse_address(value)
    except ValueError:
        raise click.BadParameter('address needs to be in format host:port')


def print_version(ctx, param, value):
    from . import __version__
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version ' + __version__)
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help='Print version and exit')
@click.option('-m', '--mode', type=click.Choice(['smtp', 'pop3', 'both']), default='both', help='Run smtp, pop3 or both (default)')
@click.option('-sa', '--smtp-address', default='localhost:5050', help='Address to run the SMTP server on. Defaults to localhost:5050', callback=validate_address)
@click.option('-pa', '--pop3-address', default='localhost:5051', help='Address to run the POP3 server on. Defaults to localhost:5051', callback=validate_address)
@click.option('-pu', '--pop3-user', default=None, help='Username for the POP3 server (default: <any>)')
@click.option('-pp', '--pop3-password', default=None, help='Password for the POP3 server (default: <any>)')
@click.argument('directory', type=click.Path(resolve_path=True), required=False)
def cli(mode, smtp_address, pop3_address, pop3_user, pop3_password, directory):
    """
    Runs an SMTP server, POP3 server or both based on a directory.

    When no directory is supplied, a temporary directory will be created and
    used. The POP3 server accepts any username and password combination by
    default.

    """
    if directory is None:
        directory = tempfile.mkdtemp()
        click.echo('Running from directory %s' % directory)
    else:
        if not os.path.exists(directory):
            os.makedirs(directory)
    store = Store(directory)
    store.load()
    if mode in ('smtp', 'both'):
        Smtp(smtp_address, None, store=store)
    if mode in ('pop3', 'both'):
        Pop3Server(pop3_address, store, pop3_user, pop3_password)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


class Smtp(SMTPServer):

    def __init__(self, *args, **kwargs):
        self.store = kwargs.pop('store')
        SMTPServer.__init__(self, *args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        self.store.save(data)
