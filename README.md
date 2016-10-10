# helpmanual


# Categories:

* `commands` - eg. things installed with `apt`
* `builtins` - eg. `compgen -b`
* pypi
* npm
* perhaps other packages managers eg. PHP, CRAN.
* specific commands git, docker, sublime, atom, aws, dropbox

## sources

* pypi
* npm
* gem
* composer/packager
* cran
* cargo
* julia pkg

## custom commands

* git
* docker
* sublime
* atom / apm
* aws-cli
* hg
* svn
* google-chrome
* chromium-browser
* nginx
* apache
* ha-proxy

# TODO

* add search
* links between pages
* add `include.h` pages.
* add json ld
* find package page came from eg. apt package
* full build command with vagrant
* use http://www.wordfrequency.info/free.asp for stopwords when generating links.

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

**Need some way of avoiding custom data being overwritten by auto generation.**

This to include in metadata:
* name
* description
* version, might end up with multiple
* source eg. apt or npm, man and man type
* data eg. man, help, version, bare call
* date generated
* data written
* author
* website
* command - used to link `compgen` to source
* path inside `./raw`
* uri
* path to any extra data for this package.
* sub commands: git, docker, apt
* perhaps some way to control cross page links

## 4. Generate html content

This is not the full page, just the content specific to each package.

Should include:
* prepare data for search index
* prepare data for sitemap.xml
* inserting links between documents

We might want to persist this data in VCS for performance and for different versions.

## 5. Generate final html pages

Create pretty HTML, not saved just sent to server, should include search index and sitemap.xml
