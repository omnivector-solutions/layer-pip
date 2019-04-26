from charms import layer

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log
from charmhelpers.fetch.python.packages import pip_install

from charms.reactive import set_flag


def install_queued_packages():
    opts = layer.options()
    if 'pip' not in opts or 'packages' not in opts['pip']:
        return

    # get requirements-parser
    pip_install('requirements-parser')
    from requirements.requirement import Requirement

    packages = opts['pip']['packages']

    for package in packages:
        pip_install(package)

        requirement = Requirement.parse(package)
        name = requirement.name
        if name:
            set_flag(f'pip.installed.{requirement.name}')
        else:
            hookenv.log(f'The name for package "{requirement.line}"'
                        ' can not be parsed', level='WARN')

    set_flag('pip.initialized')


hookenv.atstart(log, 'Initializing pip layer')
hookenv.atstart(install_queued_packages)
