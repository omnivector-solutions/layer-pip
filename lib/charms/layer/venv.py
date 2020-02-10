from subprocess import check_call
from pathlib import Path
from os import environ

from charmhelpers.core.hookenv import log, application_name
from charms.reactive import not_unless

from charms.layer import options


_cfg = options.get("venv")

ENV_NAME = _cfg["env_name"] if _cfg["env_name"] else application_name()
log("ENV_NAME: {}".format(ENV_NAME))
ENV_DIR = Path("/opt/juju_venvs") / ENV_NAME
ENV_BIN = ENV_DIR / "bin"


@not_unless("venv.active")
def call_from_env(args):
    """
    Run command with arguments from inside the venv. Wait for command
    to complete. If the return code was zero then return, otherwise
    raise CalledProcessError. The CalledProcessError object will have
    the return code in the returncode attribute.
    """
    cmd = " ".join(args)
    log("Running {} from venv".format(cmd))
    check_call(". {}/activate; {}".format(ENV_BIN, cmd), shell=True)


def pip_install(package):
    """
    Installs the given pip package from the env
    PIP uses https for upstream package downloads.
    Use the JUJU_HTTPS_PROXY if available.
    """
    cmd = []
    if "JUJU_CHARM_HTTPS_PROXY" in environ:
        cmd = ["https_proxy={}".format(environ["JUJU_CHARM_HTTPS_PROXY"])]
    cmd.extend(["pip", "install", package])
    call_from_env(cmd)
