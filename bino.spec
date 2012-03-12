Name: bino
Version: 1.2.1
Release: 3%{?dist}
Summary: 3D video player
Group: System Environment/Base
License: GPLv3+
URL: http://bino3d.org
Source0: http://download.savannah.nongnu.org/releases-noredirect/bino/%{name}-%{version}.tar.xz
# Fix for implicit DSO linkage, patch accepted by upstream
Patch1: bino-1.2.1-ld-fix.patch
# Unbundle oxygen icons
Patch2: bino-1.2.1-unbundle-icons.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: ffmpeg-devel glew-devel libass-devel openal-devel qt-devel
BuildRequires: gettext texinfo oxygen-icon-theme

%description
Bino is a 3D video player. It supports stereoscopic 3D video with a wide
variety of input and output formats. It also supports multi-display video
and it can be used for powerwalls, virtual reality installations and other
multi-projector setups.

%prep
%setup -q

# Removal of unneeded stuff
rm -rf pkg/macosx/* pkg/w32
touch pkg/macosx/Info.plist.in

# Removal of bundled oxygen-icons
rm -rf src/icons

%patch1 -p1 -b .ld-fix
%patch2 -p1 -b .unbundle-icons

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} mandir=%{_mandir}
rm -f %{buildroot}%{_infodir}/dir
mkdir _tmpdoc
mv %{buildroot}%{_datadir}/doc/%{name}/* _tmpdoc/
rm -rf %{buildroot}%{_datadir}/doc
%find_lang %{name}

%post
/sbin/install-info \
    --entry="* bino: (bino).   3D video player" \
    --section="Miscellaneous" \
    %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README _tmpdoc/*
%{_bindir}/bino
%{_infodir}/*
%{_mandir}/man1/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Thu Mar  1 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.1-3
- Unbundled oxygen icons

* Thu Mar 01 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.1-2
- Used RPM macros instead of variables
- Added requires for post and preun sections
- Removed pkg dir in prep
- Added LGPLv3+ license to license tag (oxygen icons)

* Wed Nov 09 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.1-1
- New version

* Tue Nov 01 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.3-3
- Explicit link with glew, needed if compiled with Equalizer

* Wed Sep 14 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.3-2
- Removed defattr
- Moved docs to one dir

* Sat Aug 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.3-1
- Update to new version

* Sat Aug 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.0-1
- Update to new version

* Sat Aug 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 0.9.2-1
- Initial release
