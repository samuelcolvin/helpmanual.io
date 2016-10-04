# helpmanual


# Categories:

* `commands` - eg. thing installed with `apt`
* `builtins` - eg. `compgen -b`
* pypi
* npm
* specific commands git, docker, sublime, atom, aws, dropbox

# Processing pipeline

To generate documents:

## 1. Install raw

**Skipped for now, we just use what's installed on the system.**

This will be:
* `apt install ...`
* `pip install ...`
* `npm install ...`
* specific command installs

## 2. Collect raw data

Eg. collect static files into `./raw`.

#### for man

This is simply coping and extracting. See `extract_man()`.

#### for executable commands

Run `compgen -c`, check if the command is included in `compgen -b`, apt, pip or npm installed packages.

This requires the commands to be executed with ` --help` and ` --version`,
the output can then be collected.


## 3. Update metadata

Need one metadata file summarizing what's installed and collected, but also updated here.

This to include in metadata:
* name
* description
* source eg. apt or npm
* data eg. man, help, version, bare call
* date updated
* author
* website
* sub commands: git, docker, apt
* perhaps some way to control cross page links

## 4. Generate html
