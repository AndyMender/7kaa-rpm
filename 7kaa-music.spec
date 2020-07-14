%global prj_music_dir %{_datadir}/7kaa/music
Name:     7kaa-music
Version:  2.15.3
Release:  1%{?dist}
Summary:  In-game music for Seven Kingdoms: Ancient Adversaries
BuildArch: noarch

License: Redistributable, no modification permitted
URL:      http://7kfans.com/
Source0:  https://www.7kfans.com/downloads/%{name}-2.15.tar.bz2

Supplements: 7kaa = %{version}

%description
In-Game music for Seven Kingdoms: Ancient Adversaries. Packaged separately
due to licensing.

%prep
%setup -qn %{name}

%build

%install
mkdir -p %{buildroot}%{prj_music_dir}
mkdir -p %{buildroot}%{_docdir}/%{name}

install -v -m 644 MUSIC/* %{buildroot}%{prj_music_dir}
install -v -m 644 *.txt %{buildroot}%{_docdir}/%{name}

%files
%doc README-Music.txt
%license %{_docdir}/%{name}/COPYING-Music.txt
%{prj_music_dir}/*

%changelog
* Tue May 26 2020 Andy Mender <andymenderunix@fedoraproject.org> - 2.15.3-1
- Split off music files from main 7kaa package

