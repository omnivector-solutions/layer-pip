# Pip layer

The pip layer for juju provides a convienient mechanism for
higher-layered charms to install pip packages with layer
options.

## Usage

At this time packages can only be specified to the pip layer
at charm-build time in `layer.yaml`.

```yaml
includes:
  - layer:basic
  - layer:pip
options:
  pip:
    packages:
      - left-pad
      - requirements-parser @ https://github.com/davidfischer/requirements-parser.git
```

## Flags

The pip layer will attempt to parse the name of the requirement with 
[requirements-parser](https://github.com/davidfischer/requirements-parser).

After a package is installed, if the name of a requirement can be parsed, the flag `pip.installed.{requirement_name}` will be set. Otherwise a warning will be emitted.

Once all packages are installed, the `pip.initialized` flag will be set.

## License

AGPLv3
