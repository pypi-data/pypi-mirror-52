# Portmod
![pipeline](https://gitlab.com/portmod/portmod/badges/master/pipeline.svg)
![coverage](https://gitlab.com/portmod/portmod/badges/master/coverage.svg)

A cli tool to manage mods for OpenMW

See [the Wiki](https://gitlab.com/portmod/portmod/wikis/home) for details on [Installation](https://gitlab.com/portmod/portmod/wikis/Installation/Installation) and [Setup](https://gitlab.com/portmod/portmod/wikis/Setup).

## Basic Usage

There are a number of executables installed with Portmod, however for the most part you only need to use the `omwmerge` executable.

Mods can be installed by passing the relevant atoms as command line arguments. E.g.:
`omwmerge omwllf`

You can search for mods using the `--search`/`-s` (searches name only) and `--searchdesc`/`-S` (searches name and description) options.

Specific versions of mods can be installed by including the version number: `omwmerge abandoned-flat-2.0`

Specified mods will be automatically be downloaded, configured and installed.

The `-c` flag will remove the specified mods and all mods that depend on, or are dependencies of, the specified mods.

The `-C` flag will remove the specified mods, ignoring dependencies

You can view useful information about your current setup using `omwmerge --info`.

You can update all installed mods (including dependencies and dependency changes) using the command `omwmerge --update --deep --newuse @world` (or `omwmerge -uDN @world`)
