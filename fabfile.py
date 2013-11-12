import os
from os.path import join as pjoin
from fabric.api import (env, execute, lcd, local, parallel,
                        run, roles, task)

from fabdeploytools.rpm import RPMBuild
from fabdeploytools import helpers
import fabdeploytools.envs

import deploysettings as settings


env.key_filename = settings.SSH_KEY
fabdeploytools.envs.loadenv(settings.CLUSTER)

ROOT, ADDON_REGISTRATION = helpers.get_app_dirs(__file__)

VIRTUALENV = os.path.join(ROOT, 'venv')
PYTHON = os.path.join(VIRTUALENV, 'bin', 'python')


@task
def create_virtualenv(update_on_change=False):
    helpers.create_venv(VIRTUALENV, settings.PYREPO,
                        pjoin(ADDON_REGISTRATION, 'requirements/prod.txt'),
                        update_on_change=update_on_change)


@task
def setup_install():
    with lcd(ADDON_REGISTRATION):
        local("%s setup.py install" % PYTHON)


@task
def update_info(ref='origin/master'):
    helpers.git_info(ADDON_REGISTRATION)
    with lcd(ADDON_REGISTRATION):
        local("/bin/bash -c "
              "'source /etc/bash_completion.d/git && __git_ps1'")
        local('git show -s {0} --pretty="format:%h" '
              '> media/git-rev.txt'.format(ref))


@task
@roles('celery')
@parallel
def update_celery():
    if getattr(settings, 'CELERY_SERVICE', False):
        restart = 'supervisorctl restart %s' % settings.CELERY_SERVICE
    if restarts:
        run(restart)


@task
def deploy():
    helpers.deploy(name='addon_registration',
                   env=settings.ENV,
                   cluster=settings.CLUSTER,
                   domain=settings.DOMAIN,
                   root=ROOT,
                   deploy_roles=['web', 'celery'],
                   package_dirs=['addon_registration', 'venv'])

    helpers.restart_uwsgi(getattr(settings, 'UWSGI', []))
    execute(update_celery)


@task
def pre_update(ref=settings.UPDATE_REF):
    local('date')
    execute(helpers.git_update, ADDON_REGISTRATION, ref)
    execute(update_info, ref)


@task
def update():
    execute(create_virtualenv)
    execute(setup_install)
