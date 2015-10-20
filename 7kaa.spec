%global icon_file 7kaa_icon.png
%global icon_dest_dir %{_datadir}/icons/hicolor/32x32/apps
Name:     7kaa           
Version:  2.14.5 
Release:  9%{?dist}
Summary:  Seven Kingdoms: Ancient Adversaries

License:  GPLv3+ and GPLv2+
URL:      http://7kfans.com/           
Source0:  http://sourceforge.net/projects/skfans/files/%{name}-%{version}.tar.xz
Source1:  %{name}.autodlrc
Patch0:   http://sf.net/p/skfans/bugs/4/attachment/%{name}-formatSecurity.patch

BuildRequires: SDL2-devel, SDL2_net-devel
BuildRequires: enet-devel
BuildRequires: openal-soft-devel, autoconf
BuildRequires: gettext-devel
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
Requires: %{name}-data = %{version}-%{release}

%description
Seven Kingdoms is a real-time strategy (RTS) computer game developed
by Trevor Chan of Enlight Software. The game enables players to
compete against up to six other kingdoms allowing players to conquer
opponents by defeating them in war (with troops or machines),
capturing their buildings with spies, or offering opponents money 
for their kingdom.

Seven Kingdoms: Ancient Adversaries is a free patch provided by
Interactive Magic and added three new cultures, the Egyptians, the
Mughals and the Zulus, and a new war machine, Unicorn. 

%package data
BuildArch: noarch
Summary: In-Game data Seven Kingdoms: Ancient Adversaries

Requires: %{name} = %{version}-%{release}
Requires: hicolor-icon-theme

%description data
In-Game music data Seven Kingdoms: Ancient Adversaries

%package music
License: Redistributable, no modification permitted
BuildArch: noarch
Summary: In-Game music for Seven Kingdoms: Ancient Adversaries

Requires: %{name}-data = %{version}-%{release}
Requires: autodownloader, sudo

%description music
In-Game music for Seven Kingdoms: Ancient Adversaries
Due to license issue, you need to run 7kaa-data-installer install the music.

%prep
%setup -q
%patch0 -p0 -b .formatSecurity

%build
%configure
make %{?_smp_mflags}
convert data/image/7k_icon.bmp %{icon_file}


%install
%make_install
mkdir -p %{buildroot}%{icon_dest_dir}
install -m 644 %{icon_file} %{buildroot}%{icon_dest_dir}

### == desktop file
cat>%{name}.desktop<<END
[Desktop Entry]
Name=%{name}
GenericName=Seven Kingdoms: Ancient Adversaries
Comment=A real-time strategy (RTS) computer game
Exec=/usr/bin/%{name}
Icon=%{name}_icon
Terminal=false
Type=Application
Categories=Game;StrategyGame
END

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop

### == music autodownload
%global data_installer %{name}-data-installer
%global prj_music_dir %{_datadir}/%{name}/music
mkdir -p %{buildroot}%{prj_music_dir}
mkdir -p %{buildroot}/usr/share/doc/%{name}-music

### === Downloader
cat >%{data_installer}<<END
#!/bin/bash
echo "This program will download necessary data files."
if [ -r %{prj_music_dir}/win.wav ];then
   echo "music already downloaded" > /dev/stderr
   exit 2
fi
if ! /usr/share/autodl/AutoDL.py %{prj_music_dir}/%{name}.autodlrc; then
    echo "Error on music download" > /dev/stderr
    exit 3
fi
cd /tmp/%{name}-music
tar xjvf /tmp/%{name}-music/%{name}-music.tar.bz2
sudo install -v -m 644 /tmp/%{name}-music/%{name}-music/music/* /usr/share/%{name}/music
sudo install -v -m 644 /tmp/%{name}-music/%{name}-music/*.txt /usr/share/doc/%{name}-music
echo "Done"
END

install -m 755 %{data_installer} %{buildroot}%{_bindir}/%{data_installer}
install -m 644 %{SOURCE1} %{buildroot}%{prj_music_dir}

%post data
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    if [ -x /usr/bin/gtk-update-icon-cache ];then
        /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    fi
fi

%posttrans data
if [ -x /usr/bin/gtk-update-icon-cache ];then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun music
if [ $1 -eq 0 ] ; then
## When Uninstall
    rm -fr %{prj_music_dir}
fi

%files
%doc README
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%files data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/[^m]*
%{icon_dest_dir}/%{icon_file}

%files music
%{_bindir}/%{data_installer}
%dir %{prj_music_dir}
%{prj_music_dir}/%{name}.autodlrc
%dir %{_docdir}/%{name}-music

%changelog
* Tue Oct 20 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-9
- music won't get uninstall when upgrading.

* Fri Jun 26 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-8
- Use name macro whenever possible.

* Wed Jun 24 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-7
- Fix the .desktop file.

* Tue Jun 23 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-6
- Requires: hicolor-icon-theme
- License become GPLv3+ and GPLv2+ as "gettext.h" is GPLv3

* Wed Jun 17 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-5
- Fix for Review Request Comment #11

* Tue Jun 16 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-4
- Fix for Review Request Comment #10

* Tue Jun 02 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-3
- Fix for Review Request Comment #8

* Mon Jun 01 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-2
- Fix for Review Request Comment #6

* Sun May 31 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-1
- Upstream update to 2.14.5
- BuildRequires: add enet-devel
- Use autodownloader to download music.

* Wed May 27 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.4-2
- Remove music.

* Tue May 05 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.4-1
- Initial packaging.

