%global icon_file 7kaa_icon.png
%global icon_dest_dir %{_datadir}/icons/hicolor/32x32/apps
Name:     7kaa
Version:  2.15.3
Release:  1%{?dist}
Summary:  Seven Kingdoms: Ancient Adversaries

License:  GPLv3+ and GPLv2+
URL:      http://7kfans.com/
Source0:  https://github.com/the3dfxdude/%{name}/archive/v%{version}.tar.gz
Source1:  %{name}.autodlrc

BuildRequires:  gcc-c++
BuildRequires: SDL2-devel, SDL2_net-devel
BuildRequires: enet-devel
BuildRequires: openal-soft-devel, autoconf
BuildRequires: gettext-devel
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
BuildRequires: libcurl-devel
BuildRequires: automake

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
Due to license issue, you need to run 7kaa-data-installer to install the music.

%prep
%setup -q

%build
# https://bugzilla.redhat.com/show_bug.cgi?id=1306226
export CXXFLAGS="%{optflags} -fsigned-char"
./autogen.sh
%configure
make %{?_smp_mflags}
convert data/IMAGE/7K_ICON.BMP %{icon_file}

%install
%make_install
%find_lang %{name}
mkdir -p %{buildroot}%{icon_dest_dir}
install -m 644 %{icon_file} %{buildroot}%{icon_dest_dir}

### == desktop file
cat>%{name}.desktop<<EOF
[Desktop Entry]
Name=%{name}
GenericName=Seven Kingdoms: Ancient Adversaries
Comment=A real-time strategy (RTS) computer game
Exec=%{_bindir}/%{name}
Icon=%{name}_icon
Terminal=false
Type=Application
Categories=Game;StrategyGame
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop

### == music autodownload
%global data_installer %{name}-data-installer
%global prj_music_dir %{_datadir}/%{name}/music
mkdir -p %{buildroot}%{prj_music_dir}
mkdir -p %{buildroot}%{_docdir}/%{name}-music

### === Downloader
cat >%{data_installer}<<EOF
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
sudo install -v -m 644 /tmp/%{name}-music/%{name}-music/music/* %{_datadir}/%{name}/music
sudo install -v -m 644 /tmp/%{name}-music/%{name}-music/*.txt %{_docdir}/%{name}-music
echo "Done"
EOF

install -m 755 %{data_installer} %{buildroot}%{_bindir}/%{data_installer}
install -m 644 %{SOURCE1} %{buildroot}%{prj_music_dir}

rm -f %{buildroot}%{_docdir}/%{name}/COPYING

%postun music
if [ $1 -eq 0 ] ; then
## When Uninstall
    rm -fr %{prj_music_dir}
fi

%files -f %{name}.lang
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
* Sun May 17 2020 Andy Mender <andymenderunix@fedoraproject.org> - 2.15.3-1
- Try to unorphan and update the package

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.14.7-2
- Remove obsolete scriptlets

* Thu Dec 07 2017 Ding-Yi Chen <dchen@redhat.com> - 2.14.7-1
- Upstream update to 2.14.7
  Fixes Bug 1458610 - 7kaa-2.14.7 is available
- Add Requires and BuildRequires libcurl

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 11 2017 Raphael Groner <projects.rg@smart.ms> - 2.14.6-2
- rebuilt due to branching

* Wed Mar 01 2017 Ding-Yi Chen <dchen@redhat.com> 2.14.6-1
- Upstream update to 2.14.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar 07 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.14.5-12
- Build with -fsigned-char to fix FTBFS with GCC 6 (#1306226)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 20 2015 Ding-Yi Chen <dchen@redhat.com> 2.14.5-10
- music won't get uninstall when upgrading.
- Remove /usr/share/doc/COPYING as it is already installed.

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

