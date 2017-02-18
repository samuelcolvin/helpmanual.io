#!/usr/bin/env bash
# collected by running `apt list --installed > file` and running a few regexes
set -x
sudo apt-get update
sudo apt install -y a11y-profile-manager-indicator account-plugin-facebook account-plugin-flickr account-plugin-google accountsservice
sudo apt install -y acl acpi-support acpid activity-log-manager adb adduser adium-theme-ubuntu advancecomp adwaita-icon-theme
sudo apt install -y aha aisleriot alsa-base alsa-utils anacron android-libadb android-libbase android-libcutils android-liblog
sudo apt install -y apache2-utils apg app-install-data app-install-data-partner apparmor appmenu-qt appmenu-qt5 apport apport-gtk
sudo apt install -y apport-symptoms appstream apt apt-transport-https apt-utils aptdaemon aptdaemon-data apturl apturl-common
sudo apt install -y arp-scan aspell aspell-en at at-spi2-core atom attr autotools-dev avahi-autoipd avahi-daemon avahi-utils
sudo apt install -y bamfdaemon baobab base-files base-passwd bash bash-completion bbswitch-dkms bc bind9-host binfmt-support
sudo apt install -y binutils bluez bluez-cups bluez-obexd branding-ubuntu bridge-utils brltty bsdmainutils bsdtar bsdutils
sudo apt install -y build-essential bundler busybox-initramfs busybox-static bzip2 bzip2-doc ca-certificates ca-certificates-java
sudo apt install -y ca-certificates-mono ccze cdparanoia cgroupfs-mount checkbox-converged checkbox-gui checkinstall cheese
sudo apt install -y cheese-common chromium-browser chromium-browser-l10n chromium-codecs-ffmpeg-extra clang clang-3.8 cli-common
sudo apt install -y cloc cmake cmake-data colord colord-data colordiff comerr-dev command-not-found command-not-found-data
sudo apt install -y compiz compiz-core compiz-gnome compiz-plugins compiz-plugins-default compiz-plugins-extra console-setup
sudo apt install -y console-setup-linux containerd coreutils cpio cpp cpp-5 cracklib-runtime crda crip cron cryptsetup cryptsetup-bin
sudo apt install -y csh cssc cups cups-browsed cups-bsd cups-client cups-common cups-core-drivers cups-daemon cups-filters
sudo apt install -y cups-filters-core-drivers cups-pk-helper cups-ppdc cups-server-common curl cvs cvsps dash dbus dbus-x11
sudo apt install -y dc dconf-cli dconf-gsettings-backend dconf-service dctrl-tools debconf debconf-i18n debhelper debianutils
sudo apt install -y default-jre default-jre-headless deja-dup desktop-file-utils devscripts dh-python dh-strip-nondeterminism
sudo apt install -y dialog dictionaries-common diffmerge diffstat diffutils dirmngr distro-info-data dkms dmeventd dmidecode
sudo apt install -y dmsetup dmz-cursor-theme dns-root-data dnsmasq-base dnsutils doc-base docbook-xml docker.io dosfstools
sudo apt install -y dpkg dpkg-dev e2fslibs e2fsprogs ed efibootmgr eject emacs emacs24 emacs24-bin-common emacs24-common
sudo apt install -y emacs24-common-non-dfsg emacs24-el emacsen-common enchant eog esound-common espeak-data ethtool evemu-tools
sudo apt install -y evince evince-common evolution-data-server evolution-data-server-common evolution-data-server-online-accounts
sudo apt install -y evtest example-content expect extlinux fakeroot fbset ffmpeg fftw2 file file-roller findutils firefox
sudo apt install -y firefox-locale-en flac flake flashplugin-installer fontconfig fontconfig-config fonts-dejavu-core fonts-dejavu-extra
sudo apt install -y fonts-freefont-ttf fonts-guru fonts-guru-extra fonts-kacst fonts-kacst-one fonts-khmeros-core fonts-lao
sudo apt install -y fonts-lato fonts-liberation fonts-lklug-sinhala fonts-lmodern fonts-lohit-guru fonts-lyx fonts-nanum
sudo apt install -y fonts-noto-cjk fonts-opendin fonts-opensymbol fonts-roboto fonts-roboto-hinted fonts-sil-abyssinica fonts-sil-padauk
sudo apt install -y fonts-stix fonts-symbola fonts-takao-pgothic fonts-texgyre fonts-thai-tlwg fonts-tibetan-machine fonts-tlwg-garuda
sudo apt install -y fonts-tlwg-garuda-ttf fonts-tlwg-kinnari fonts-tlwg-kinnari-ttf fonts-tlwg-laksaman fonts-tlwg-laksaman-ttf
sudo apt install -y fonts-tlwg-loma fonts-tlwg-loma-ttf fonts-tlwg-mono fonts-tlwg-mono-ttf fonts-tlwg-norasi fonts-tlwg-norasi-ttf
sudo apt install -y fonts-tlwg-purisa fonts-tlwg-purisa-ttf fonts-tlwg-sawasdee fonts-tlwg-sawasdee-ttf fonts-tlwg-typewriter
sudo apt install -y fonts-tlwg-typewriter-ttf fonts-tlwg-typist fonts-tlwg-typist-ttf fonts-tlwg-typo fonts-tlwg-typo-ttf
sudo apt install -y fonts-tlwg-umpush fonts-tlwg-umpush-ttf fonts-tlwg-waree fonts-tlwg-waree-ttf foomatic-db-compressed-ppds
sudo apt install -y freebsd-manpages freepats friendly-recovery ftp fuse fwupd fwupdate fwupdate-signed g++ g++-5 gamin gawk
sudo apt install -y gcc gcc-5 gcc-5-base gcc-6-base gcolor2 gconf-service gconf-service-backend gconf2 gconf2-common gcr
sudo apt install -y gdb gdbserver gdebi-core gdisk gedit gedit-common genisoimage geoclue geoclue-ubuntu-geoip geoip-bin
sudo apt install -y geoip-database gettext gettext-base ghostscript ghostscript-x gimp-data gir1.2-accounts-1.0 gir1.2-appindicator3-0.1
sudo apt install -y gir1.2-atk-1.0 gir1.2-atspi-2.0 gir1.2-dbusmenu-glib-0.4 gir1.2-dee-1.0 gir1.2-freedesktop gir1.2-gdata-0.0
sudo apt install -y gir1.2-gdkpixbuf-2.0 gir1.2-glib-2.0 gir1.2-gnomekeyring-1.0 gir1.2-goa-1.0 gir1.2-gst-plugins-base-1.0
sudo apt install -y gir1.2-gstreamer-1.0 gir1.2-gtk-3.0 gir1.2-gtksource-3.0 gir1.2-gudev-1.0 gir1.2-ibus-1.0 gir1.2-javascriptcoregtk-4.0
sudo apt install -y gir1.2-json-1.0 gir1.2-notify-0.7 gir1.2-packagekitglib-1.0 gir1.2-pango-1.0 gir1.2-peas-1.0 gir1.2-rb-3.0
sudo apt install -y gir1.2-secret-1 gir1.2-signon-1.0 gir1.2-soup-2.4 gir1.2-totem-1.0 gir1.2-totem-plparser-1.0 gir1.2-udisks-2.0
sudo apt install -y gir1.2-unity-5.0 gir1.2-vte-2.91 gir1.2-webkit2-4.0 gir1.2-wnck-3.0 git git-all git-arch git-core git-crypt
sudo apt install -y git-cvs git-doc git-el git-email git-extras git-flow git-ftp git-gui git-man git-mediawiki git-repair
sudo apt install -y git-sh git-svn gitg gitk gitweb gkbd-capplet gksu glib-networking glib-networking-common glib-networking-services
sudo apt install -y gnome-accessibility-themes gnome-bluetooth gnome-calculator gnome-calendar gnome-desktop3-data gnome-disk-utility
sudo apt install -y gnome-font-viewer gnome-keyring gnome-mahjongg gnome-menus gnome-mines gnome-orca gnome-power-manager
sudo apt install -y gnome-screensaver gnome-screenshot gnome-session-bin gnome-session-canberra gnome-session-common gnome-settings-daemon-schemas
sudo apt install -y gnome-software gnome-software-common gnome-sudoku gnome-system-log gnome-system-monitor gnome-terminal
sudo apt install -y gnome-terminal-data gnome-user-guide gnome-user-share gnome-video-effects gnupg gnupg-agent gnupg2 golang-1.6-go
sudo apt install -y golang-1.6-race-detector-runtime golang-1.6-src golang-go golang-race-detector-runtime golang-src google-chrome-stable
sudo apt install -y gparted gpgv gpick gramofile grap grep grilo-plugins-0.2-base groff groff-base grub-common grub-efi-amd64
sudo apt install -y grub-efi-amd64-bin grub-efi-amd64-signed grub2-common gsettings-desktop-schemas gsettings-ubuntu-schemas
sudo apt install -y gsfonts gstreamer1.0-alsa gstreamer1.0-clutter-3.0 gstreamer1.0-fluendo-mp3 gstreamer1.0-libav gstreamer1.0-plugins-bad
sudo apt install -y gstreamer1.0-plugins-bad-faad gstreamer1.0-plugins-bad-videoparsers gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
sudo apt install -y gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-ugly-amr gstreamer1.0-pulseaudio
sudo apt install -y gstreamer1.0-tools gstreamer1.0-x gtk2-engines-murrine gucharmap guile-2.0-libs gvfs gvfs-bin gvfs-common
sudo apt install -y gvfs-daemons gvfs-fuse gvfs-libs gzip haproxy hardening-includes hdparm heroku heroku-toolbelt hicolor-icon-theme
sudo apt install -y hostname hplip hplip-data hud humanity-icon-theme hunspell-en-us hwdata hyphen-en-us i965-va-driver ibus
sudo apt install -y ibus-gtk ibus-gtk3 ibus-table icu-devtools ifupdown im-config imagemagick imagemagick-6.q16 imagemagick-common
sudo apt install -y indicator-application indicator-appmenu indicator-bluetooth indicator-datetime indicator-keyboard indicator-messages
sudo apt install -y indicator-power indicator-printers indicator-session indicator-sound info init init-system-helpers initramfs-tools
sudo apt install -y initramfs-tools-bin initramfs-tools-core initscripts inkscape inotify-tools inputattach insserv install-info
sudo apt install -y intel-gpu-tools intel-microcode intltool-debian ippusbxd iproute2 iptables iputils-arping iputils-ping
sudo apt install -y iputils-tracepath irqbalance isc-dhcp-client isc-dhcp-common iso-codes iucode-tool iw java-common javascript-common
sudo apt install -y jayatana julia julia-common kbd kerneloops-daemon keyboard-configuration klibc-utils kmod krb5-locales
sudo apt install -y krb5-multidev ksh language-pack-en language-pack-en-base language-pack-gnome-en language-pack-gnome-en-base
sudo apt install -y language-selector-common language-selector-gnome laptop-detect lcov less lib32gcc1 liba11y-profile-manager-0.1-0
sudo apt install -y liba11y-profile-manager-data liba52-0.7.4 libaa1 libaacs0 libabw-0.1-1v5 libaccount-plugin-1.0-0 libaccount-plugin-generic-oauth
sudo apt install -y libaccount-plugin-google libaccounts-glib0 libaccounts-qt5-1 libaccountsservice0 libacl1 libaec0 libaio1
sudo apt install -y libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libamd2.4.1 libandroid-properties1
sudo apt install -y libao-common libao4 libapparmor-perl libapparmor1 libappindicator1 libappindicator3-1 libappstream-glib8
sudo apt install -y libappstream3 libapr1 libaprutil1 libapt-inst2.0 libapt-pkg-perl libapt-pkg5.0 libarchive-zip-perl libarchive13
sudo apt install -y libarmadillo6 libarpack2 libart-2.0-2 libasan2 libasn1-8-heimdal libasound2 libasound2-data libasound2-plugins
sudo apt install -y libaspell15 libasprintf-dev libasprintf0v5 libass5 libassuan0 libasyncns0 libatasmart4 libatk-adaptor
sudo apt install -y libatk-bridge2.0-0 libatk1.0-0 libatk1.0-data libatkmm-1.6-1v5 libatm1 libatomic1 libatspi2.0-0 libattr1
sudo apt install -y libaudio2 libaudiofile1 libaudit-common libaudit1 libauthen-sasl-perl libavahi-client3 libavahi-common-data
sudo apt install -y libavahi-common3 libavahi-core7 libavahi-glib1 libavahi-ui-gtk3-0 libavc1394-0 libavcodec-dev libavcodec-ffmpeg56
sudo apt install -y libavdevice-ffmpeg56 libavfilter-ffmpeg5 libavformat-dev libavformat-ffmpeg56 libavresample-ffmpeg2 libavutil-dev
sudo apt install -y libavutil-ffmpeg54 libbabeltrace-ctf1 libbabeltrace1 libbamf3-2 libbasicusageenvironment1 libbdplus0
sudo apt install -y libbind9-140 libblas-common libblas3 libblkid1 libbluetooth3 libbluray1 libbonobo2-0 libbonobo2-common
sudo apt install -y libbonoboui2-0 libbonoboui2-common libboost-all-dev libboost-atomic-dev libboost-atomic1.58-dev libboost-atomic1.58.0
sudo apt install -y libboost-chrono-dev libboost-chrono1.58-dev libboost-chrono1.58.0 libboost-context-dev libboost-context1.58-dev
sudo apt install -y libboost-context1.58.0 libboost-coroutine-dev libboost-coroutine1.58-dev libboost-coroutine1.58.0 libboost-date-time-dev
sudo apt install -y libboost-date-time1.58-dev libboost-date-time1.58.0 libboost-dev libboost-exception-dev libboost-exception1.58-dev
sudo apt install -y libboost-filesystem-dev libboost-filesystem1.58-dev libboost-filesystem1.58.0 libboost-graph-dev libboost-graph-parallel-dev
sudo apt install -y libboost-graph-parallel1.58-dev libboost-graph-parallel1.58.0 libboost-graph1.58-dev libboost-graph1.58.0
sudo apt install -y libboost-iostreams-dev libboost-iostreams1.58-dev libboost-iostreams1.58.0 libboost-locale-dev libboost-locale1.58-dev
sudo apt install -y libboost-locale1.58.0 libboost-log-dev libboost-log1.58-dev libboost-log1.58.0 libboost-math-dev libboost-math1.58-dev
sudo apt install -y libboost-math1.58.0 libboost-mpi-dev libboost-mpi-python-dev libboost-mpi-python1.58-dev libboost-mpi-python1.58.0
sudo apt install -y libboost-mpi1.58-dev libboost-mpi1.58.0 libboost-program-options-dev libboost-program-options1.58-dev
sudo apt install -y libboost-program-options1.58.0 libboost-python-dev libboost-python1.58-dev libboost-python1.58.0 libboost-random-dev
sudo apt install -y libboost-random1.58-dev libboost-random1.58.0 libboost-regex-dev libboost-regex1.58-dev libboost-regex1.58.0
sudo apt install -y libboost-serialization-dev libboost-serialization1.58-dev libboost-serialization1.58.0 libboost-signals-dev
sudo apt install -y libboost-signals1.58-dev libboost-signals1.58.0 libboost-system-dev libboost-system1.58-dev libboost-system1.58.0
sudo apt install -y libboost-test-dev libboost-test1.58-dev libboost-test1.58.0 libboost-thread-dev libboost-thread1.58-dev
sudo apt install -y libboost-thread1.58.0 libboost-timer-dev libboost-timer1.58-dev libboost-timer1.58.0 libboost-tools-dev
sudo apt install -y libboost-wave-dev libboost-wave1.58-dev libboost-wave1.58.0 libboost1.58-dev libboost1.58-tools-dev libbrlapi0.6
sudo apt install -y libbs2b0 libbsd0 libbz2-1.0 libbz2-dev libc-bin libc-dev-bin libc6 libc6-dbg libc6-dev libc6-i386 libcaca0
sudo apt install -y libcairo-gobject2 libcairo-perl libcairo2 libcairomm-1.0-1v5 libcamd2.4.1 libcamel-1.2-54 libcanberra-gtk-module
sudo apt install -y libcanberra-gtk0 libcanberra-gtk3-0 libcanberra-gtk3-module libcanberra-pulse libcanberra0 libcap-ng0
sudo apt install -y libcap2 libcap2-bin libcc1-0 libccolamd2.9.1 libcddb-get-perl libcddb2 libcdio-cdda1 libcdio-paranoia1
sudo apt install -y libcdio13 libcdparanoia0 libcdr-0.1-1 libcgi-fast-perl libcgi-pm-perl libcgmanager0 libcheese-gtk25 libcheese8
sudo apt install -y libcholmod3.0.6 libchromaprint0 libcilkrts5 libclang-common-3.8-dev libclang1-3.8 libclass-accessor-perl
sudo apt install -y libclass-factory-util-perl libclass-singleton-perl libclone-perl libclucene-contribs1v5 libclucene-core1v5
sudo apt install -y libclutter-1.0-0 libclutter-1.0-common libclutter-gst-3.0-0 libclutter-gtk-1.0-0 libcmis-0.5-5v5 libcogl-common
sudo apt install -y libcogl-pango20 libcogl-path20 libcogl20 libcolamd2.9.1 libcolord2 libcolorhug2 libcolumbus1-common libcolumbus1v5
sudo apt install -y libcomerr2 libcommon-sense-perl libcompizconfig0 libconfig-inifiles-perl libcrack2 libcroco3 libcryptsetup4
sudo apt install -y libcrystalhd3 libctemplate2v5 libcuda1-370 libcups2 libcupscgi1 libcupsfilters1 libcupsimage2 libcupsmime1
sudo apt install -y libcupsppdc1 libcurl3 libcurl3-gnutls libdaemon0 libdap17v5 libdapclient6v5 libdata-alias-perl libdatetime-format-builder-perl
sudo apt install -y libdatetime-format-iso8601-perl libdatetime-format-strptime-perl libdatetime-locale-perl libdatetime-perl
sudo apt install -y libdatetime-timezone-perl libdatrie1 libdb5.3 libdbd-sqlite3-perl libdbi-perl libdbi1 libdbus-1-3 libdbus-glib-1-2
sudo apt install -y libdbusmenu-glib4 libdbusmenu-gtk3-4 libdbusmenu-gtk4 libdbusmenu-qt2 libdbusmenu-qt5 libdc1394-22 libdca0
sudo apt install -y libdconf1 libde265-0 libdebconfclient0 libdecoration0 libdee-1.0-4 libdevmapper-event1.02.1 libdevmapper1.02.1
sudo apt install -y libdfu1 libdigest-hmac-perl libdirectfb-1.2-9 libdistro-info-perl libdjvulibre-text libdjvulibre21 libdmapsharing-3.0-2
sudo apt install -y libdns-export162 libdns162 libdotconf0 libdouble-conversion1v5 libdpkg-perl libdrm-amdgpu1 libdrm-intel1
sudo apt install -y libdrm-nouveau2 libdrm-nouveau2-dbg libdrm-radeon1 libdrm2 libdsfmt-19937-1 libdv4 libdvbpsi10 libdvdnav4
sudo apt install -y libdvdread4 libe-book-0.1-1 libebackend-1.2-10 libebml4v5 libebook-1.2-16 libebook-contacts-1.2-2 libecal-1.2-19
sudo apt install -y libedata-book-1.2-25 libedata-cal-1.2-28 libedataserver-1.2-21 libedataserverui-1.2-1 libedit2 libefivar0
sudo apt install -y libegl1-mesa libelf1 libemail-valid-perl libenchant1c2a libencode-locale-perl libeot0 libepoxy0 libepsilon1
sudo apt install -y libept1.5.0 liberror-perl libesd0 libespeak1 libestr0 libetonyek-0.1-1 libev4 libevdev2 libevdocument3-4
sudo apt install -y libevemu3 libevent-2.0-5 libevent-core-2.0-5 libevview3-3 libexempi3 libexif12 libexiv2-14 libexpat1
sudo apt install -y libexpat1-dev libexporter-tiny-perl libexttextcat-2.0-0 libexttextcat-data libfaad2 libfakeroot libfcgi-perl
sudo apt install -y libfcitx-config4 libfcitx-gclient0 libfcitx-utils0 libfdisk1 libffi-dev libffi6 libfftw3-double3 libfftw3-single3
sudo apt install -y libfile-basedir-perl libfile-copy-recursive-perl libfile-desktopentry-perl libfile-fcntllock-perl libfile-listing-perl
sudo apt install -y libfile-mimeinfo-perl libfile-stripnondeterminism-perl libfile-type-perl libflac8 libflite1 libfluidsynth1
sudo apt install -y libfont-afm-perl libfont-ttf-perl libfontconfig1 libfontconfig1-dev libfontembed1 libfontenc1 libframe6
sudo apt install -y libfreehand-0.1-1 libfreerdp-cache1.1 libfreerdp-client1.1 libfreerdp-codec1.1 libfreerdp-common1.1.0
sudo apt install -y libfreerdp-core1.1 libfreerdp-crypto1.1 libfreerdp-gdi1.1 libfreerdp-locale1.1 libfreerdp-plugins-standard
sudo apt install -y libfreerdp-primitives1.1 libfreerdp-utils1.1 libfreetype6 libfreetype6-dev libfreexl1 libfribidi0 libfuse2
sudo apt install -y libfwup0 libfwupd1 libgail-3-0 libgail-common libgail18 libgamin0 libgbm1 libgc1c2 libgcab-1.0-0 libgcc-5-dev
sudo apt install -y libgcc1 libgck-1-0 libgconf-2-4 libgconf2.0-cil libgcr-3-common libgcr-base-3-1 libgcr-ui-3-1 libgcrypt20
sudo apt install -y libgd-perl libgd3 libgdal1i libgdata-common libgdata22 libgdbm3 libgdiplus libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-common
sudo apt install -y libgee-0.8-2 libgeis1 libgeoclue0 libgeocode-glib0 libgeoip1 libgeonames0 libgeos-3.5.0 libgeos-c1v5
sudo apt install -y libgetopt-argvfile-perl libgettextpo-dev libgettextpo0 libgexiv2-2 libgfortran3 libgif7 libgimp2.0 libgirepository-1.0-1
sudo apt install -y libgit2-24 libgit2-glib-1.0-0 libgksu2-0 libgl1-mesa-dri libgl1-mesa-glx libglade2-0 libglapi-mesa libgles1-mesa
sudo apt install -y libgles2-mesa libglew1.13 libglewmx1.13 libglib-perl libglib2.0-0 libglib2.0-bin libglib2.0-cil libglib2.0-data
sudo apt install -y libglibmm-2.4-1v5 libglu1-mesa libgme0 libgmime-2.6-0 libgmp-dev libgmp10 libgmpxx4ldbl libgnome-2-0
sudo apt install -y libgnome-bluetooth13 libgnome-desktop-3-12 libgnome-keyring-common libgnome-keyring0 libgnome-menu-3-0
sudo apt install -y libgnome2-0 libgnome2-bin libgnome2-common libgnomecanvas2-0 libgnomecanvas2-common libgnomekbd-common
sudo apt install -y libgnomekbd8 libgnomeui-0 libgnomeui-common libgnomevfs2-0 libgnomevfs2-common libgnomevfs2-extra libgnutls-openssl27
sudo apt install -y libgnutls30 libgoa-1.0-0b libgoa-1.0-common libgom-1.0-0 libgom-1.0-common libgomp1 libgpg-error0 libgpgme11
sudo apt install -y libgphoto2-6 libgphoto2-l10n libgphoto2-port12 libgpm2 libgpod-common libgpod4 libgrail6 libgraphite2-3
sudo apt install -y libgrilo-0.2-1 libgroupsock8 libgs9 libgs9-common libgsettings-qt1 libgsl2 libgsm1 libgssapi-krb5-2 libgssapi3-heimdal
sudo apt install -y libgssrpc4 libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-good1.0-0
sudo apt install -y libgstreamer1.0-0 libgtk-3-0 libgtk-3-bin libgtk-3-common libgtk2-perl libgtk2.0-0 libgtk2.0-bin libgtk2.0-cil
sudo apt install -y libgtk2.0-common libgtkglext1 libgtkmm-2.4-1v5 libgtkmm-3.0-1v5 libgtksourceview-3.0-1 libgtksourceview-3.0-common
sudo apt install -y libgtkspell0 libgtkspell3-3-0 libgtop-2.0-10 libgtop2-common libgucharmap-2-90-7 libgudev-1.0-0 libgusb2
sudo apt install -y libgutenprint2 libgweather-3-6 libgweather-common libgxps2 libhardware2 libharfbuzz-icu0 libharfbuzz0b
sudo apt install -y libhcrypto4-heimdal libhdf4-0-alt libhdf5-10 libheimbase1-heimdal libheimntlm0-heimdal libhogweed4 libhpmud0
sudo apt install -y libhtml-form-perl libhtml-format-perl libhtml-parser-perl libhtml-tagset-perl libhtml-template-perl libhtml-tree-perl
sudo apt install -y libhttp-cookies-perl libhttp-daemon-perl libhttp-date-perl libhttp-message-perl libhttp-negotiate-perl
sudo apt install -y libhttp-parser2.1 libhud2 libhunspell-1.3-0 libhwloc-dev libhwloc-plugins libhwloc5 libhx509-5-heimdal
sudo apt install -y libhybris libhybris-common1 libhyphen0 libibus-1.0-5 libibverbs-dev libibverbs1 libical1a libice6 libicsharpcode-nrefactory-cecil5.0-cil
sudo apt install -y libicsharpcode-nrefactory-csharp5.0-cil libicsharpcode-nrefactory5.0-cil libicu-dev libicu55 libidn11
sudo apt install -y libido3-0.1-0 libiec61883-0 libieee1284-3 libijs-0.35 libilmbase12 libimage-magick-perl libimage-magick-q16-perl
sudo apt install -y libimage-size-perl libimobiledevice6 libindicator3-7 libindicator7 libinotifytools0 libinput10 libio-html-perl
sudo apt install -y libio-pty-perl libio-socket-inet6-perl libio-socket-ssl-perl libio-string-perl libipc-run-perl libipc-system-simple-perl
sudo apt install -y libirs141 libisc-export160 libisc160 libisccc140 libisccfg140 libisl15 libiso9660-8 libitm1 libiw30 libjack-jackd2-0
sudo apt install -y libjansson4 libjasper1 libjavascriptcoregtk-4.0-18 libjbig0 libjbig2dec0 libjemalloc1 libjpeg-dev libjpeg-turbo8
sudo apt install -y libjpeg-turbo8-dev libjpeg8 libjpeg8-dev libjs-jquery libjson-c2 libjson-glib-1.0-0 libjson-glib-1.0-common
sudo apt install -y libjson-perl libjson-xs-perl libjsoncpp1 libk5crypto3 libkadm5clnt-mit9 libkadm5srv-mit9 libkate1 libkdb5-8
sudo apt install -y libkeyutils1 libklibc libkmlbase1 libkmldom1 libkmlengine1 libkmod2 libkpathsea6 libkrb5-26-heimdal libkrb5-3
sudo apt install -y libkrb5support0 libksba8 liblangtag-common liblangtag1 liblapack3 liblcms2-2 liblcms2-utils libldap-2.4-2
sudo apt install -y liblept5 liblightdm-gobject-1-0 liblinear3 liblircclient0 liblist-moreutils-perl liblivemedia50 libllvm3.8
sudo apt install -y liblocale-gettext-perl liblockfile-bin liblockfile1 liblouis-data liblouis9 liblouisutdml-bin liblouisutdml-data
sudo apt install -y liblouisutdml6 liblqr-1-0 liblsan0 libltdl-dev libltdl7 liblua5.1-0 liblua5.2-0 liblua5.3-0 libluajit-5.1-2
sudo apt install -y libluajit-5.1-common liblvm2app2.2 liblvm2cmd2.02 liblwp-mediatypes-perl liblwp-protocol-https-perl liblwres141
sudo apt install -y liblz4-1 liblzma5 liblzo2-2 libm17n-0 libmad0 libmagic1 libmagick++-6.q16-5v5 libmagickcore-6.q16-2 libmagickcore-6.q16-2-extra
sudo apt install -y libmagickwand-6.q16-2 libmail-sendmail-perl libmailtools-perl libmatroska6v5 libmbim-glib4 libmbim-proxy
sudo apt install -y libmedia1 libmediaart-2.0-0 libmediawiki-api-perl libmessaging-menu0 libmetacity-private3a libmhash2
sudo apt install -y libmimic0 libminiupnpc10 libminizip1 libmirclient9 libmircommon5 libmirprotobuf3 libmjpegutils-2.1-0
sudo apt install -y libmm-glib0 libmms0 libmng2 libmnl0 libmodplug1 libmodule-implementation-perl libmodule-runtime-perl
sudo apt install -y libmono-cairo4.0-cil libmono-cecil-private-cil libmono-corlib4.5-cil libmono-i18n-west4.0-cil libmono-i18n4.0-cil
sudo apt install -y libmono-posix4.0-cil libmono-security4.0-cil libmono-system-configuration4.0-cil libmono-system-core4.0-cil
sudo apt install -y libmono-system-drawing4.0-cil libmono-system-security4.0-cil libmono-system-xml4.0-cil libmono-system4.0-cil
sudo apt install -y libmount1 libmp3lame0 libmpc3 libmpcdec6 libmpdec2 libmpeg2-4 libmpeg2encpp-2.1-0 libmpfr4 libmpg123-0
sudo apt install -y libmplex2-2.1-0 libmpx0 libmspub-0.1-1 libmtdev1 libmtp-common libmtp-runtime libmtp9 libmwaw-0.3-3 libmysqlclient-dev
sudo apt install -y libmysqlclient20 libmysqlcppconn7v5 libmythes-1.2-0 libnatpmp1 libnautilus-extension1a libncurses5 libncurses5-dev
sudo apt install -y libncursesw5 libncursesw5-dev libndp0 libneon27-gnutls libnet-dbus-perl libnet-dns-perl libnet-domain-tld-perl
sudo apt install -y libnet-http-perl libnet-ip-perl libnet-libidn-perl libnet-smtp-ssl-perl libnet-ssleay-perl libnetcdf11
sudo apt install -y libnetfilter-conntrack3 libnetpbm10 libnettle6 libnewt0.52 libnfnetlink0 libnghttp2-14 libnghttp2-dev
sudo apt install -y libnih-dbus1 libnih1 libnl-3-200 libnl-genl-3-200 libnm-glib-vpn1 libnm-glib4 libnm-gtk-common libnm-gtk0
sudo apt install -y libnm-util2 libnm0 libnma-common libnma0 libnotify-bin libnotify4 libnpth0 libnspr4 libnss-mdns libnss3
sudo apt install -y libnss3-nssdb libnuma-dev libnuma1 libnux-4.0-0 libnux-4.0-common liboauth0 libobjc-5-dev libobjc4 libodbc1
sudo apt install -y libodfgen-0.1-1 libofa0 libogdi3.2 libogg0 libopenal-data libopenal1 libopenblas-base libopencore-amrnb0
sudo apt install -y libopencore-amrwb0 libopencv-calib3d2.4v5 libopencv-contrib2.4v5 libopencv-core2.4v5 libopencv-features2d2.4v5
sudo apt install -y libopencv-flann2.4v5 libopencv-highgui2.4v5 libopencv-imgproc2.4v5 libopencv-legacy2.4v5 libopencv-ml2.4v5
sudo apt install -y libopencv-objdetect2.4v5 libopencv-video2.4v5 libopenexr22 libopenjp2-7 libopenjpeg5 libopenlibm2 libopenmpi-dev
sudo apt install -y libopenmpi1.10 libopenspecfun1 libopus0 liborbit-2-0 liborc-0.4-0 liborcus-0.10-0v5 libotf0 liboxideqt-qmlplugin
sudo apt install -y liboxideqtcore0 liboxideqtquick0 libp11-kit-gnome-keyring libp11-kit0 libpackage-deprecationmanager-perl
sudo apt install -y libpackage-stash-perl libpackage-stash-xs-perl libpackagekit-glib2-16 libpagemaker-0.0-0 libpam-gnome-keyring
sudo apt install -y libpam-modules libpam-modules-bin libpam-runtime libpam-systemd libpam0g libpango-1.0-0 libpango-perl
sudo apt install -y libpango1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpangomm-1.4-1v5 libpangox-1.0-0 libpangoxft-1.0-0
sudo apt install -y libpaper-utils libpaper1 libparams-classify-perl libparams-util-perl libparams-validate-perl libparse-debianchangelog-perl
sudo apt install -y libparted-fs-resize0 libparted2 libpcap0.8 libpci3 libpciaccess0 libpcre16-3 libpcre2-8-0 libpcre3 libpcrecpp0v5
sudo apt install -y libpcsclite1 libpdf-api2-perl libpeas-1.0-0 libpeas-1.0-0-python3loader libpeas-common libperl5.22 libperlio-gzip-perl
sudo apt install -y libpipeline1 libpixman-1-0 libplist3 libplymouth4 libpng12-0 libpng12-dev libpolkit-agent-1-0 libpolkit-backend-1-0
sudo apt install -y libpolkit-gobject-1-0 libpoppler-glib8 libpoppler58 libpopt0 libportaudio2 libpostproc-ffmpeg53 libpotrace0
sudo apt install -y libpq-dev libpq5 libprocps4 libproj9 libprotobuf-lite9v5 libprotobuf9v5 libproxy-tools libproxy1-plugin-gsettings
sudo apt install -y libproxy1-plugin-networkmanager libproxy1v5 libptexenc1 libpthread-stubs0-dev libpulse-mainloop-glib0
sudo apt install -y libpulse0 libpulsedsp libpwquality-common libpwquality1 libpython-all-dev libpython-dev libpython-stdlib
sudo apt install -y libpython2.7 libpython2.7-dev libpython2.7-minimal libpython2.7-stdlib libpython3-dev libpython3-stdlib
sudo apt install -y libpython3.4 libpython3.4-dev libpython3.4-minimal libpython3.4-stdlib libpython3.5 libpython3.5-dev
sudo apt install -y libpython3.5-minimal libpython3.5-stdlib libpython3.6 libpython3.6-dev libpython3.6-minimal libpython3.6-stdlib
sudo apt install -y libqmi-glib1 libqmi-proxy libqpdf17 libqqwing2v5 libqt4-dbus libqt4-declarative libqt4-network libqt4-opengl
sudo apt install -y libqt4-script libqt4-sql libqt4-sql-sqlite libqt4-xml libqt4-xmlpatterns libqt5core5a libqt5dbus5 libqt5feedback5
sudo apt install -y libqt5gui5 libqt5multimedia5 libqt5network5 libqt5opengl5 libqt5organizer5 libqt5positioning5 libqt5printsupport5
sudo apt install -y libqt5qml5 libqt5quick5 libqt5quicktest5 libqt5sql5 libqt5sql5-sqlite libqt5svg5 libqt5test5 libqt5webkit5
sudo apt install -y libqt5widgets5 libqt5x11extras5 libqt5xml5 libqtcore4 libqtdbus4 libqtgui4 libquadmath0 libquvi-scripts
sudo apt install -y libquvi7 libraptor2-0 librarian0 librasqal3 libraw1394-11 libraw15 librdf0 libreadline-dev libreadline5
sudo apt install -y libreadline6 libreadline6-dev libregexp-common-perl libreoffice-avmedia-backend-gstreamer libreoffice-base-core
sudo apt install -y libreoffice-calc libreoffice-common libreoffice-core libreoffice-draw libreoffice-gnome libreoffice-gtk
sudo apt install -y libreoffice-help-en-us libreoffice-impress libreoffice-math libreoffice-ogltrans libreoffice-pdfimport
sudo apt install -y libreoffice-style-breeze libreoffice-style-galaxy libreoffice-writer libresid-builder0c2a librest-0.7-0
sudo apt install -y librevenge-0.0-0 librhythmbox-core9 libroken18-heimdal librrd4 librsvg2-2 librsvg2-bin librsvg2-common
sudo apt install -y librsvg2-doc librtmp1 libruby2.3 libsamplerate0 libsane libsane-common libsane-hpaio libsasl2-2 libsasl2-modules
sudo apt install -y libsasl2-modules-db libsbc1 libschroedinger-1.0-0 libsdl-image1.2 libsdl-ttf2.0-0 libsdl1.2debian libseccomp2
sudo apt install -y libsecret-1-0 libsecret-common libselinux1 libsemanage-common libsemanage1 libsensors4 libsepol1 libserf-1-1
sudo apt install -y libsgutils2-2 libshine3 libshout3 libshp-dev libshp2 libsidplay1v5 libsidplay2v5 libsigc++-2.0-0v5 libsignon-extension1
sudo apt install -y libsignon-glib1 libsignon-plugins-common1 libsignon-qt5-1 libsigsegv2 libslang2 libsm6 libsmartcols1
sudo apt install -y libsnapd-glib1 libsnappy1v5 libsndfile1 libsnmp-base libsnmp30 libsocket6-perl libsodium18 libsonic0
sudo apt install -y libsoundtouch1 libsoup-gnome2.4-1 libsoup2.4-1 libsox-fmt-alsa libsox-fmt-base libsox2 libsoxr0 libspandsp2
sudo apt install -y libspatialite7 libspdylay7 libspectre1 libspeechd2 libspeex1 libspeexdsp1 libspqr2.0.2 libsqlite3-0 libsqlite3-dev
sudo apt install -y libsrtp0 libss2 libssh-4 libssh-gcrypt-4 libssh2-1 libssl-dev libssl-doc libssl1.0.0 libstartup-notification0
sudo apt install -y libstdc++-5-dev libstdc++6 libsub-install-perl libsub-name-perl libsuitesparseconfig4.4.6 libsuperlu4
sudo apt install -y libsvn-perl libsvn1 libswresample-dev libswresample-ffmpeg1 libswscale-dev libswscale-ffmpeg3 libsynctex1
sudo apt install -y libsys-hostname-long-perl libsystemd0 libsz2 libtag1v5 libtag1v5-vanilla libtasn1-6 libtbb2 libtcl8.5
sudo apt install -y libtcl8.6 libtcltk-ruby libtdb1 libtelepathy-glib0 libterm-readkey-perl libterm-readline-perl-perl libtesseract3
sudo apt install -y libtexlua52 libtexluajit2 libtext-charwidth-perl libtext-iconv-perl libtext-levenshtein-perl libtext-wrapi18n-perl
sudo apt install -y libthai-data libthai0 libtheora0 libtie-ixhash-perl libtiff5 libtimedate-perl libtimezonemap-data libtimezonemap1
sudo apt install -y libtinfo-dev libtinfo5 libtinyxml2.6.2v5 libtk8.5 libtk8.6 libtool libtotem-plparser-common libtotem-plparser18
sudo apt install -y libtotem0 libtracker-sparql-1.0-0 libtry-tiny-perl libtsan0 libtwolame0 libtxc-dxtn-s2tc0 libtypes-serialiser-perl
sudo apt install -y libubsan0 libubuntugestures5 libubuntutoolkit5 libudev1 libudisks2-0 libumfpack5.7.1 libunistring0 libunity-action-qt1
sudo apt install -y libunity-control-center1 libunity-core-6.0-9 libunity-gtk2-parser0 libunity-gtk3-parser0 libunity-misc4
sudo apt install -y libunity-protocol-private0 libunity-scopes-json-def-desktop libunity-settings-daemon1 libunity-webapps0
sudo apt install -y libunity9 libunwind8 libupnp6 libupower-glib3 liburi-perl liburiparser1 liburl-dispatcher1 libusageenvironment3
sudo apt install -y libusb-0.1-4 libusb-1.0-0 libusbmuxd4 libustr-1.0-1 libutempter0 libutf8proc1 libuuid-perl libuuid1 libv4l-0
sudo apt install -y libv4lconvert0 libva-drm1 libva-x11-1 libva1 libvcdinfo0 libvdpau1 libvisio-0.1-1 libvisual-0.4-0 libvlc5
sudo apt install -y libvlccore8 libvncclient1 libvo-aacenc0 libvo-amrwbenc0 libvorbis0a libvorbisenc2 libvorbisfile3 libvpx3
sudo apt install -y libvsqlitepp3v5 libvte-2.91-0 libvte-2.91-common libwacom-bin libwacom-common libwacom2 libwavpack1 libwayland-client0
sudo apt install -y libwayland-cursor0 libwayland-egl1-mesa libwayland-server0 libwebkit2gtk-4.0-37 libwebkit2gtk-4.0-37-gtk2
sudo apt install -y libwebp5 libwebpmux1 libwebrtc-audio-processing-0 libwhoopsie-preferences0 libwhoopsie0 libwildmidi-config
sudo apt install -y libwildmidi1 libwind0-heimdal libwinpr-crt0.1 libwinpr-dsparse0.1 libwinpr-environment0.1 libwinpr-file0.1
sudo apt install -y libwinpr-handle0.1 libwinpr-heap0.1 libwinpr-input0.1 libwinpr-interlocked0.1 libwinpr-library0.1 libwinpr-path0.1
sudo apt install -y libwinpr-pool0.1 libwinpr-registry0.1 libwinpr-rpc0.1 libwinpr-sspi0.1 libwinpr-synch0.1 libwinpr-sysinfo0.1
sudo apt install -y libwinpr-thread0.1 libwinpr-utils0.1 libwmf-bin libwmf0.2-7 libwmf0.2-7-gtk libwnck-3-0 libwnck-3-common
sudo apt install -y libwpd-0.10-10 libwpg-0.3-3 libwps-0.4-4 libwrap0 libwww-perl libwww-robotrules-perl libwxbase3.0-0v5
sudo apt install -y libwxgtk3.0-0v5 libx11-6 libx11-data libx11-dev libx11-doc libx11-protocol-perl libx11-xcb1 libx264-148
sudo apt install -y libx265-79 libx86-1 libxapian22v5 libxatracker2 libxau-dev libxau6 libxaw7 libxcb-composite0 libxcb-dri2-0
sudo apt install -y libxcb-dri3-0 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-present0 libxcb-randr0 libxcb-render-util0
sudo apt install -y libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 libxcb-xkb1 libxcb-xv0
sudo apt install -y libxcb1 libxcb1-dev libxcomposite1 libxcursor1 libxdamage1 libxdmcp-dev libxdmcp6 libxdo3 libxerces-c3.1
sudo apt install -y libxext6 libxfixes3 libxfont1 libxft2 libxi6 libxinerama1 libxkbcommon-x11-0 libxkbcommon0 libxkbfile1
sudo apt install -y libxklavier16 libxml-parser-perl libxml-twig-perl libxml-xpathengine-perl libxml2 libxml2-dev libxml2-utils
sudo apt install -y libxmu6 libxmuu1 libxnvctrl0 libxpm4 libxrandr2 libxrender-dev libxrender1 libxres1 libxshmfence1 libxslt1-dev
sudo apt install -y libxslt1.1 libxss1 libxt6 libxtables11 libxtst6 libxv1 libxvidcore4 libxvmc1 libxxf86dga1 libxxf86vm1
sudo apt install -y libyajl2 libyaml-0-2 libyaml-dev libyaml-libyaml-perl libyaml-perl libyaml-tiny-perl libyelp0 libzbar0
sudo apt install -y libzeitgeist-1.0-1 libzeitgeist-2.0-0 libzip4 libzmq5 libzopfli-dev libzopfli1 libzvbi-common libzvbi0
sudo apt install -y libzzip-0-13 light-themes lightdm lighttpd lintian linux-base linux-firmware linux-generic linux-headers-4.4.0-59
sudo apt install -y linux-headers-4.4.0-59-generic linux-headers-4.4.0-62 linux-headers-4.4.0-62-generic linux-headers-generic
sudo apt install -y linux-image-4.4.0-59-generic linux-image-4.4.0-62-generic linux-image-extra-4.4.0-59-generic linux-image-extra-4.4.0-62-generic
sudo apt install -y linux-image-generic linux-libc-dev linux-signed-generic linux-signed-image-4.4.0-59-generic linux-signed-image-4.4.0-62-generic
sudo apt install -y linux-signed-image-generic linux-sound-base livemedia-utils llvm llvm-3.8 llvm-3.8-dev llvm-3.8-runtime
sudo apt install -y llvm-runtime lmodern locales locate login logrotate lp-solve lsb-base lsb-release lshw lsof ltrace lua-lpeg
sudo apt install -y lua5.2 luajit lvm2 lynx lynx-common lzop m17n-db make makedev man-db man2html man2html-base manpages
sudo apt install -y manpages-dev manpages-posix manpages-posix-dev mawk media-player-info memtest86+ menu mesa-vdpau-drivers
sudo apt install -y metacity-common mime-support mlocate mobile-broadband-provider-info modemmanager mokutil mono-4.0-gac
sudo apt install -y mono-gac mono-runtime mono-runtime-common mono-runtime-sgen moreutils motion mount mountall mousetweaks
sudo apt install -y mpi-default-bin mpi-default-dev mscompress mtools mtr-tiny multiarch-support mysql-client mysql-client-5.7
sudo apt install -y mysql-client-core-5.7 mysql-common mysql-server mysql-server-5.7 mysql-server-core-5.7 mysql-utilities
sudo apt install -y mysql-workbench mysql-workbench-data mythes-en-us nano nautilus nautilus-data nautilus-sendto nautilus-share
sudo apt install -y ncompress ncurses-base ncurses-bin ncurses-term net-tools netbase netcat-openbsd netpbm network-manager
sudo apt install -y network-manager-gnome network-manager-pptp network-manager-pptp-gnome nghttp2 nghttp2-client nghttp2-proxy
sudo apt install -y nghttp2-server nmap nodejs notify-osd notify-osd-icons ntfs-3g numactl nux-tools nvidia-370 nvidia-opencl-icd-370
sudo apt install -y nvidia-prime nvidia-settings ocl-icd-libopencl1 odbcinst odbcinst1debian2 onboard onboard-data openbsd-inetd
sudo apt install -y openjdk-8-jre openjdk-8-jre-headless openmpi-bin openmpi-common openoffice.org-hyphenation openprinting-ppds
sudo apt install -y openssh-client openssh-server openssh-sftp-server openssl os-prober overlay-scrollbar overlay-scrollbar-gtk2
sudo apt install -y oxideqt-codecs-extra p11-kit p11-kit-modules p7zip-full pandoc pandoc-data parted passwd patch patchutils
sudo apt install -y pciutils pcmciautils pdfmod pencil2d perl perl-base perl-doc perl-modules-5.22 pgadmin3 pgadmin3-data
sudo apt install -y pgagent pinentry-gnome3 pkg-config plainbox-provider-checkbox plainbox-provider-resource-generic plainbox-secure-policy
sudo apt install -y plymouth plymouth-label plymouth-theme-ubuntu-logo plymouth-theme-ubuntu-text pm-utils po-debconf pod2pdf
sudo apt install -y policykit-1 policykit-1-gnome policykit-desktop-privileges poppler-data poppler-utils popularity-contest
sudo apt install -y postfix postgresql postgresql-9.5 postgresql-client postgresql-client-9.5 postgresql-client-common postgresql-common
sudo apt install -y postgresql-contrib postgresql-contrib-9.5 postgresql-server-dev-9.5 powermgmt-base ppp pppconfig pppoeconf
sudo apt install -y pptp-linux printer-driver-brlaser printer-driver-c2esp printer-driver-foo2zjs printer-driver-foo2zjs-common
sudo apt install -y printer-driver-gutenprint printer-driver-hpcups printer-driver-min12xxw printer-driver-pnm2ppa printer-driver-postscript-hp
sudo apt install -y printer-driver-ptouch printer-driver-pxljr printer-driver-sag-gdi printer-driver-splix procps proj-bin
sudo apt install -y proj-data psmisc psutils pulseaudio pulseaudio-module-bluetooth pulseaudio-module-x11 pulseaudio-utils
sudo apt install -y pycharm pyotherside pypy pypy-lib python python-apt-common python-bs4 python-chardet python-crypto python-dev
sudo apt install -y python-ecdsa python-html5lib python-lxml python-minimal python-mysql.connector python-numpy python-paramiko
sudo apt install -y python-pexpect python-pip-whl python-pkg-resources python-ptyprocess python-pygments python-pyodbc python-pysqlite2
sudo apt install -y python-six python2.7 python2.7-dev python2.7-minimal python3 python3-apport python3-apt python3-aptdaemon
sudo apt install -y python3-aptdaemon.gtk3widgets python3-aptdaemon.pkcompat python3-blinker python3-brlapi python3-bs4 python3-cairo
sudo apt install -y python3-cffi-backend python3-chardet python3-checkbox-support python3-commandnotfound python3-cryptography
sudo apt install -y python3-cups python3-cupshelpers python3-dbus python3-debian python3-defer python3-dev python3-distupgrade
sudo apt install -y python3-feedparser python3-gdbm python3-gi python3-gi-cairo python3-guacamole python3-html5lib python3-httplib2
sudo apt install -y python3-idna python3-jinja2 python3-jwt python3-louis python3-lxml python3-magic python3-mako python3-markupsafe
sudo apt install -y python3-minimal python3-oauthlib python3-padme python3-pexpect python3-pil python3-pip python3-pkg-resources
sudo apt install -y python3-plainbox python3-problem-report python3-ptyprocess python3-pyasn1 python3-pyatspi python3-pycurl
sudo apt install -y python3-pyparsing python3-renderpm python3-reportlab python3-reportlab-accel python3-requests python3-setuptools
sudo apt install -y python3-six python3-software-properties python3-speechd python3-systemd python3-uno python3-update-manager
sudo apt install -y python3-urllib3 python3-virtualenv python3-wheel python3-xdg python3-xkit python3-xlsxwriter python3.4
sudo apt install -y python3.4-dev python3.4-minimal python3.5 python3.5-dev python3.5-minimal python3.6 python3.6-dev python3.6-minimal
sudo apt install -y qdbus qml-module-io-thp-pyotherside qml-module-qt-labs-folderlistmodel qml-module-qt-labs-settings qml-module-qtfeedback
sudo apt install -y qml-module-qtgraphicaleffects qml-module-qtquick-layouts qml-module-qtquick-window2 qml-module-qtquick2
sudo apt install -y qml-module-qttest qml-module-ubuntu-components qml-module-ubuntu-layouts qml-module-ubuntu-onlineaccounts
sudo apt install -y qml-module-ubuntu-performancemetrics qml-module-ubuntu-test qml-module-ubuntu-web qmlscene qpdf qt-at-spi
sudo apt install -y qtchooser qtcore4-l10n qtdeclarative5-accounts-plugin qtdeclarative5-dev-tools qtdeclarative5-qtquick2-plugin
sudo apt install -y qtdeclarative5-test-plugin qtdeclarative5-ubuntu-ui-toolkit-plugin qtdeclarative5-unity-action-plugin
sudo apt install -y qttranslations5-l10n rake rarian-compat readline-common redis-server redis-tools remmina remmina-common
sudo apt install -y remmina-plugin-rdp remmina-plugin-vnc rename resolvconf rfkill rhythmbox rhythmbox-data rhythmbox-plugin-zeitgeist
sudo apt install -y rhythmbox-plugins ri rrdtool rsh-client rsh-server rsync rsyslog rtkit ruby ruby-atk ruby-bundler ruby-cairo
sudo apt install -y ruby-childprocess ruby-dev ruby-did-you-mean ruby-domain-name ruby-erubis ruby-ffi ruby-full ruby-gdk-pixbuf2
sudo apt install -y ruby-gettext ruby-glib2 ruby-gtk2 ruby-http-cookie ruby-i18n ruby-listen ruby-locale ruby-log4r ruby-mime-types
sudo apt install -y ruby-minitest ruby-molinillo ruby-net-http-persistent ruby-net-scp ruby-net-sftp ruby-net-ssh ruby-net-telnet
sudo apt install -y ruby-netrc ruby-nokogiri ruby-pango ruby-power-assert ruby-rb-inotify ruby-rest-client ruby-sqlite3 ruby-test-unit
sudo apt install -y ruby-text ruby-thor ruby-unf ruby-unf-ext ruby2.3 ruby2.3-dev ruby2.3-doc ruby2.3-tcltk rubygems-integration
sudo apt install -y runc sane sane-utils sbsigntool screen-resolution-extra screenruler sdb seahorse secureboot-db sed sensible-utils
sudo apt install -y session-migration session-shortcuts sessioninstaller setserial sgml-base sgml-data shared-mime-info sharutils
sudo apt install -y shim shim-signed shotwell shotwell-common signon-keyring-extension signon-plugin-oauth2 signon-plugin-password
sudo apt install -y signon-ui signon-ui-service signon-ui-x11 signond simple-scan sl snap-confine snapd snapd-login-service
sudo apt install -y sni-qt software-properties-common software-properties-gtk sound-theme-freedesktop sox spawn-fcgi speech-dispatcher
sudo apt install -y speech-dispatcher-audio-plugins sqlite3 squashfs-tools ssh-import-id ssl-cert strace sublime-text subversion
sudo apt install -y subversion-toolssudo suru-icon-theme synaptic syslinux syslinux-common syslinux-legacy sysstat system-config-printer-common
sudo apt install -y system-config-printer-gnome system-config-printer-udev systemd systemd-sysv sysv-rc sysvinit-utils t1utils
sudo apt install -y tar tcl tcl-expect tcl8.6 tcl8.6-dev tcl8.6-doc tcpd tcpdump tcpflow telnet tesseract-ocr tesseract-ocr-eng
sudo apt install -y tesseract-ocr-equ tesseract-ocr-osd tex-common tex-gyre texlive-base texlive-binaries texlive-fonts-recommended
sudo apt install -y texlive-fonts-recommended-doc texlive-latex-base texlive-latex-base-doc texlive-latex-recommended texlive-latex-recommended-doc
sudo apt install -y thermald thunderbird thunderbird-gnome-support thunderbird-locale-en thunderbird-locale-en-us time tipa
sudo apt install -y tk tk8.6 tla tla-doc toshset totem totem-common totem-plugins traceroute transfig transmission-common
sudo apt install -y transmission-gtk tree ttf-ancient-fonts-symbola ttf-bitstream-vera ttf-ubuntu-font-family tth-common
sudo apt install -y tzdata ubuntu-artwork ubuntu-core-launcher ubuntu-desktop ubuntu-docs ubuntu-drivers-common ubuntu-fan
sudo apt install -y ubuntu-keyring ubuntu-mobile-icons ubuntu-mono ubuntu-release-upgrader-core ubuntu-release-upgrader-gtk
sudo apt install -y ubuntu-restricted-addons ubuntu-session ubuntu-settings ubuntu-software ubuntu-sounds ubuntu-standard
sudo apt install -y ubuntu-system-service ubuntu-touch-sounds ubuntu-ui-toolkit-theme ubuntu-wallpapers ubuntu-wallpapers-xenial
sudo apt install -y ucf udev udisks2 ufw unattended-upgrades unetbootin unetbootin-translations unity unity-accessibility-profiles
sudo apt install -y unity-asset-pool unity-control-center unity-control-center-faces unity-control-center-signon unity-greeter
sudo apt install -y unity-gtk-module-common unity-gtk2-module unity-gtk3-module unity-lens-applications unity-lens-files
sudo apt install -y unity-lens-music unity-lens-photos unity-lens-video unity-schemas unity-scope-calculator unity-scope-chromiumbookmarks
sudo apt install -y unity-scope-colourlovers unity-scope-devhelp unity-scope-firefoxbookmarks unity-scope-gdrive unity-scope-home
sudo apt install -y unity-scope-manpages unity-scope-openclipart unity-scope-texdoc unity-scope-tomboy unity-scope-video-remote
sudo apt install -y unity-scope-virtualbox unity-scope-yelp unity-scope-zotero unity-scopes-master-default unity-scopes-runner
sudo apt install -y unity-services unity-settings-daemon unity-webapps-common unity-webapps-qml unity-webapps-service uno-libs3
sudo apt install -y unzip update-inetd update-manager update-manager-core update-notifier update-notifier-common upower upstart
sudo apt install -y ure ureadahead usb-creator-common usb-creator-gtk usb-modeswitch usb-modeswitch-data usbmuxd usbutils
sudo apt install -y util-linux uuid-runtime va-driver-all vagrant vbetool vdpau-driver-all vdpau-va-driver vim vim-common
sudo apt install -y vim-gnome vim-gui-common vim-nox vim-runtime vim-tiny vino virtualbox-5.0 virtualenv visual-studio-code
sudo apt install -y vlc vlc-data vlc-nox vlc-plugin-notify vorbis-tools vorbisgain wamerican wbritish wdiff webapp-container
sudo apt install -y webbrowser-app wget whiptail whois whoopsie whoopsie-preferences wireless-regdb wireless-tools wodim
sudo apt install -y wordnet wordnet-base wordnet-gui wpasupplicant wrk x11-apps x11-common x11-session-utils x11-utils x11-xkb-utils
sudo apt install -y x11-xserver-utils x11proto-core-dev x11proto-input-dev x11proto-kb-dev x11proto-render-dev xauth xbitmaps
sudo apt install -y xbrlapi xclip xcursor-themes xdg-user-dirs xdg-user-dirs-gtk xdg-utils xdiagnose xdm xdotool xfonts-base
sudo apt install -y xfonts-encodings xfonts-scalable xfonts-utils xinit xinput xkb-data xml-core xmltoman xorg xorg-docs-core
sudo apt install -y xorg-sgml-doctools xsane xsane-common xserver-common xserver-xorg xserver-xorg-core xserver-xorg-input-all
sudo apt install -y xserver-xorg-input-evdev xserver-xorg-input-synaptics xserver-xorg-input-vmmouse xserver-xorg-input-wacom
sudo apt install -y xserver-xorg-video-all xserver-xorg-video-amdgpu xserver-xorg-video-ati xserver-xorg-video-fbdev xserver-xorg-video-intel
sudo apt install -y xserver-xorg-video-nouveau xserver-xorg-video-nouveau-dbg xserver-xorg-video-qxl xserver-xorg-video-radeon
sudo apt install -y xserver-xorg-video-vesa xserver-xorg-video-vmware xterm xtrans-dev xul-ext-ubufox xvfb xz-utils yelp
sudo apt install -y yelp-xsl zcash zeitgeist-core zeitgeist-datahub zenity zenity-common zip zlib1g zlib1g-dev zopfli zsh zsh-common

sudo apt-get upgrade -y
