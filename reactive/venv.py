from subprocess import check_call

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log

from charms.reactive import set_flag

from charms.layer import options
from charms.layer.venv import pip_install, ENV_DIR


def init():
    log('Initializing venv layer')
    cfg = options.get('venv')

    # pip does not install properly to venvs created inside
    # the charm env, so we use the system-installed python
    # as a work around.
    check_call(['/usr/bin/python3', '-m', 'venv', str(ENV_DIR)])

    # venv.create(str(ENV_DIR), with_pip=True)
    set_flag('venv.active')

    for package in cfg['packages']:
        pip_install(package)

    set_flag('venv.ready')


hookenv.atstart(init)
