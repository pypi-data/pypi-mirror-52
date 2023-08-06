# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# stdlib imports
import os
from os.path import join

# 3rd party imports
from alembic import command
from alembic.config import Config as AlembicConfig
from peltak.core import conf
from peltak.core import log


DEFAULT_ALEMBIC_CONFIG = 'migrations/alembic.ini'
DEFAULT_ALEMBIC_DIR = 'migrations'


def init_migrations():
    alembic_config = conf.get_path('db.alembic.config', DEFAULT_ALEMBIC_CONFIG)
    alembic_dir = conf.get_path('db.alembic.dir', DEFAULT_ALEMBIC_DIR)

    with conf.within_proj_dir():
        config = AlembicConfig(conf.proj_path(alembic_config))
        command.init(config, alembic_dir)

    log.info('Remember to configure <33>sqlalchemy.url <32>in <34>{}'.format(
        alembic_config
    ))

    log.info('If you want the migration auto-generation to work you need to '
             'configure <33>target_metadata <32>in <34>{}/env.py'.format(
        alembic_dir
    ))


def make_migration(message, no_auto):
    """ Create a new migration. """
    alembic_config = conf.get('db.alembic.config', DEFAULT_ALEMBIC_CONFIG)

    with conf.within_proj_dir():
        rev_id = _get_current_revision()
        config = AlembicConfig(conf.proj_path(alembic_config))
        command.revision(
            config,
            message,
            autogenerate=not no_auto,
            rev_id='{0:05}'.format(rev_id + 1)
        )


def migrate(revision):
    """ Run all pending migrations. """
    alembic_config = conf.get('db.alembic_config', DEFAULT_ALEMBIC_CONFIG)

    with conf.within_proj_dir():
        config = AlembicConfig(conf.proj_path(alembic_config))
        command.upgrade(config, revision)


def _get_current_revision():
    alembic_dir = conf.get_path('db.alembic.dir', DEFAULT_ALEMBIC_DIR)
    migrations_dir = join(alembic_dir, 'versions')
    revisions = [x.split('_', 1)[0] for x in os.listdir(migrations_dir)]
    revisions = sorted(revisions)

    if revisions:
        return int(revisions[-1])

    return 0
