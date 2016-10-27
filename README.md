# helpmanual

To deploy

```
./node_modules/.bin/webpack --progress --colors --optimize-minimize
python src/50_build_site.py
aws s3 --profile personal sync site/ s3://helpmanual.io/ --acl public-read
```

To watch js:
```
./node_modules/.bin/webpack --progress --colors --watch
```

## sources

apt packages with man pages:

* manpages-posix-dev
* freebsd-manpages
* avh-libc

* pypi
* npm
* gem
* https://www.staticgen.com/ top 10
* go
* composer/packager
* cran
* cargo
* julia pkg

## more commands

* postfix

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

## more man pages

https://www.freebsd.org/cgi/man.cgi/faq.html

# TODO

* find cross links
  * resolve 404s
  * add scroll spy
* remove render blocking css above the fold
* add posix page as tab and change search badge

* man to text fixes eg. `"\fBnpm-logout\fR - Log out of the registry"`
* links between pages
* add `include.h` page links.
* add "installed via" and package info pages
* add json ld
* full build command with vagrant
* find package page came from eg. apt package
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
