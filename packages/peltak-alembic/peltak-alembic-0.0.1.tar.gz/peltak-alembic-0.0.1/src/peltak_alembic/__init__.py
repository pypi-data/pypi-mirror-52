# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
__version__ = '0.0.1'

# 3rd party imports
from peltak.commands import click, root_cli


@root_cli.group('db')
def db_cli():
    """ Database related commands. """
    pass


@db_cli.command('init')
def init_migrations():
    from . import impl
    impl.init_migrations()


@db_cli.command('make-migration')
@click.argument('message')
@click.option(
    '--no-auto',
    is_flag=True,
    help="If given, it will not auto generate the migration from the database."
)
def make_migration(message, no_auto):
    """ Create a new migration. """
    from . import impl
    impl.make_migration(message, no_auto)


@db_cli.command('migrate')
@click.option(
    '-r',
    '--revision',
    type=str,
    default='head',
    help="Target revision"
)
def migrate(revision):
    """ Run all pending migrations. """
    from . import impl
    impl.migrate(revision)
