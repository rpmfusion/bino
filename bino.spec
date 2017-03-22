Name:    bino
Version: 1.6.5
Release: 1%{?dist}
Summary: 3D video player
Group:   System Environment/Base
License: GPLv3+
URL:     http://bino3d.org
Source0: http://download.savannah.nongnu.org/releases/bino/%{name}-%{version}.tar.xz
Patch0:  revert_glewmx.patch

# No libquadmath-devel on ARM
ExcludeArch: armhfp armv7hl

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info
Requires:        hicolor-icon-theme

BuildRequires: automake
BuildRequires: ffmpeg-devel
BuildRequires: glew-devel
BuildRequires: libass-devel
BuildRequires: openal-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libquadmath-devel
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: oxygen-icon-theme
BuildRequires: desktop-file-utils

%description
Bino is a 3D video player. It supports stereoscopic 3D video with a wide
variety of input and output formats. It also supports multi-display video
and it can be used for powerwalls, virtual reality installations and other
multi-projector setups.

%prep
%autosetup -p1
# Needed for revert_glewmx.patch
mkdir m4
autoreconf -fiv

# Removal of unneeded stuff
rm -rf pkg/macosx/*
touch pkg/macosx/Info.plist.in

%build
%configure --with-qt-version=5
%{make_build}

%install
%{make_install}
rm -f %{buildroot}%{_infodir}/dir

mkdir _tmpdoc
mv %{buildroot}%{_datadir}/doc/%{name}/* _tmpdoc/
rm -rf %{buildroot}%{_datadir}/doc

desktop-file-validate %{buildroot}%{_datadir}/applications/bino.desktop

%find_lang %{name}

%post
/sbin/install-info \
    --entry="* bino: (bino).   3D video player" \
    --section="Miscellaneous" \
    %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-desktop-database &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README _tmpdoc/*
%license COPYING
%{_bindir}/bino
%{_infodir}/*
%{_mandir}/man1/*
%{_datadir}/applications/bino.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Wed Mar 22 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.6.5-1
- New version
- Patch for glew-2.0 changes

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.6.4-1
- New version
  Resolves: rfbz#4366
- Dropped ffmpeg_2.9 patch (upstreamed)

* Tue Aug 16 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.3-3
- Add requires hicolor-icon-theme (rfbz#4191)
- Add mime scriptlets

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.6.3-2
- Rebuilt for ffmpeg-3.1.1

* Sat Jul 09 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.3-1
- update to 1.6.3 release
- patch for ffmpeg-3.0
- switch to qt5
- add exclude armhfp

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 1.4.4-6
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.4.4-5
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1.4.4-4
- Rebuilt for ffmpeg-2.3

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1.4.4-3
- Rebuilt for ffmpeg-2.3

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 1.4.4-2
- Rebuilt for ffmpeg-2.2

* Wed Nov 27 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.4-1
- New version

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-4
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-3
- Rebuilt for FFmpeg 2.0.x

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-2
- Rebuilt for x264/FFmpeg

* Thu May 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2-1
- New version
- Workarounded FTBFS due to glew fedora bug rhbz#966649
  Resolves: rfbz#2774

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-2
- Rebuilt for FFmpeg 1.0

* Thu Oct 18 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-1
- New version
- Dropped ld-fix patch (upstreamed)
- Dropped unbundle-icons patch (not needed)

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-4
- Rebuilt for FFmpeg

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
