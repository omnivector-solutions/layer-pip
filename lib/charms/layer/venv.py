from subprocess import check_call
from pathlib import Path

from charmhelpers.core.hookenv import log, charm_dir
from charms.reactive import not_unless

from charms.layer import options


_cfg = options.get('venv')


if _cfg['env-dir']:
    ENV_DIR = Path(_cfg['env-dir'])
else:
    ENV_DIR = Path(charm_dir()) / 'venv'

ENV_BIN = ENV_DIR / 'bin'


@not_unless('venv.active')
def call_from_env(args):
    """
    Run command with arguments from inside the venv. Wait for command
    to complete. If the return code was zero then return, otherwise
    raise CalledProcessError. The CalledProcessError object will have
    the return code in the returncode attribute.
    """
    cmd = ' '.join(args)
    log(f'Running {cmd} from venv')
    check_call(['bash', '-c', f'source {ENV_DIR}/bin/activate\n{cmd}'])


def pip_install(package):
    """
    Installs the give pip package from the env
    """
    call_from_env(['pip', 'install', package])
