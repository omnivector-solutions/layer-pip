import distro
from subprocess import check_call

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log
from charms.reactive import set_flag, clear_flag, when, when_not, helpers
from charms.layer import options

from charms.layer.venv import pip_install, ENV_DIR, ENV_NAME, ENV_BIN


@when_not("venv.active")
def init():
    log("Initializing venv layer")
    if not ENV_DIR.exists():
        ENV_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)

    if not ENV_BIN.exists():
        # pip does not install properly to venvs created inside
        # the charm env, so we use the system-installed python
        # as a work around.

        # On Ubuntu older than bionic, venv doesn't support --prompt
        if distro.id() == "ubuntu" and int(distro.version_parts()[0]) < 18:
            check_call(["/usr/bin/python3", "-m", "venv", str(ENV_DIR)])
        else:
            check_call(["/usr/bin/python3", "-m", "venv", "--prompt", ENV_NAME, str(ENV_DIR)])

    # venv.create(str(ENV_DIR), with_pip=True)
    set_flag("venv.active")


@when("venv.active", "venv.ready")
def reconfigure():
    cfg = options.get("venv")
    if "packages" in cfg:
        if helpers.data_changed("venv-packages", cfg["packages"]):
            clear_flag("venv.ready")
    if helpers.data_changed("venv-name", ENV_NAME):
        clear_flag("venv.active")


@when("venv.active")
@when_not("venv.ready")
def add_pip_to_venv():
    cfg = options.get("venv")
    for package in cfg["packages"]:
        pip_install(package)

    set_flag("venv.ready")


hookenv.atstart(init)
