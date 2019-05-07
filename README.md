# venv layer

The venv layer for juju provides a convienient mechanism for
charms to install pip packages in a python3 venv.

## Usage

At this time packages can only be specified to the pip layer
at charm-build time in `layer.yaml`.

```yaml
includes:
  - layer:basic
  - layer:venv
options:
  venv:
    packages:
      - left-pad
      - requirements-parser @ https://github.com/davidfischer/requirements-parser.git
    env_name: myenv
```

## Flags

The `venv.active` flag is set once the virtual env is created, and
the `venv.ready` flag is set once all packages listed in the options
are installed.

## License

AGPLv3
