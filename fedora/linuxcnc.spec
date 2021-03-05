# https://copr.fedorainfracloud.org/coprs/spike/linuxcnc/

%global commit d1982f1db4b1a40d3f21724790cb43737a310570
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

Name:          linuxcnc
Version:       2.9.0
Release:       1.20210305git%{shortcommit}%{?dist}
Summary:       LinuxCNC
License:       GPLv2+ and LGPLv2
URL:           http://linuxcnc.org/
Source0:       https://github.com/LinuxCNC/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch:         fix_install-alt.patch
Patch:         python3_compatibility_persistence.py.patch
Patch:         python3_compatibility_popupkeyboard.py.patch
BuildRequires: automake gcc-c++
BuildRequires: pkgconfig(libudev) pkgconfig(libusb-1.0) pkgconfig(libtirpc)
BuildRequires: pkgconfig(glib-2.0) pkgconfig(gtk+-2.0)
BuildRequires: procps kmod python3-Yapps intltool findutils tcl-devel tk-devel
BuildRequires: bwidget tkimg tclx python3-gobject readline-devel python3-tkinter
BuildRequires: boost-python3-devel libGLU-devel libXmu-devel psmisc python3-devel
BuildRequires: desktop-file-utils ImageMagick

Requires: tcl-%{name} = %{version}
Requires: python-%{name} = %{version}
Requires: bwidget, python3-tkinter, boost-python3, tkimg, pygtk2
AutoReq: no

%description
LinuxCNC controls CNC machines. It can drive milling machines, lathes,
3d printers, laser cutters, plasma cutters, robot arms, hexapods, and more.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
Development files for %{name}

%package doc
Summary: Documementation for %{name}
Buildarch: noarch

%description doc
Documementation for %{name}

%package -n tcl-%{name}
Summary: Tcl files for %{name}
Provides: tcl(Hal) tcl(Linuxcnc) tcl(Ngcgui)

%description -n tcl-%{name}
Tcl files for %{name}

%package -n python-%{name}
Summary: Python files for %{name}
AutoReq: no

%description -n python-%{name}
Python files for %{name}

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
export CPPFLAGS="$(pkg-config --cflags python3)"

sed -i 's#lib/tcltk/linuxcnc#%{tcl_sitearch}/linuxcnc%{version}#g' \
    lib/python/rs274/options.py

pushd src
sed -i -e 's#\(EMC2_TCL_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_TCL_LIB_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_LANG_DIR=\)${prefix}/share/linuxcnc/tcl/msgs#\1%{tcl_sitearch}/linuxcnc/tcl/msgs#g' \
       -e 's#\(EMC2_RTLIB_DIR=\)${prefix}/lib/linuxcnc#\1%{_libdir}/linuxcnc#g' \
       configure.ac

autoreconf -ifv
%configure --disable-build-documentation \
           --enable-non-distributable=yes \
           --without-libmodbus \
           --with-realtime=uspace \
           --with-boost-python=boost_python%{python3_version_nodots} \
           --with-python=%{__python3}

%make_build

%install
pushd src
%make_install SITEPY=%{python3_sitelib}
popd

# move X11 app-defaults to the correct location
mv %{buildroot}%{_sysconfdir}/X11 %{buildroot}%{_datadir}/

# remove duplicated .so files
rm -f %{buildroot}%{_libdir}/{compat.so,hal.so,rtapi.so,shmcommon.so}

# install icon files
for x in 16 32 48; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$x'x'$x/apps
    convert linuxcncicon.png -resize $x'x'$x \
            %{buildroot}%{_datadir}/icons/hicolor/$x'x'$x/apps/linuxcncicon.png
done

# install desktop files
for app in debian/extras/usr/share/applications/*.desktop; do
    desktop-file-install \
      --dir %{buildroot}%{_datadir}/applications \
      ${app}
done

# correct tcl/tk installation directory
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_prefix}/lib/tcltk/linuxcnc %{buildroot}%{tcl_sitearch}/linuxcnc%{version}
rm -rf %{buildroot}%{_prefix}/lib/tcltk

# TODO: qtpyvcp is not python3 compatible yet
# https://github.com/LinuxCNC/linuxcnc/issues/819
rm -rf %{buildroot}%{python3_sitelib}/qtvcp
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" %{buildroot}/usr/share/qtvcp/screens/qtdragon/qtdragon_handler.py

%find_lang %{name}
%find_lang gmoccapy

%files -f gmoccapy.lang -f %{name}.lang
%{_bindir}/*
%{_prefix}/lib/%{name}
%{_sysconfdir}/%{name}
%{_sysconfdir}/init.d/realtime
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/X11/app-defaults/*
%{_libdir}/*
%exclude %{_libdir}/*.a
%{_datadir}/%{name}
%{_datadir}/axis
%{_datadir}/glade3
%{_datadir}/gmoccapy
%{_datadir}/gscreen
%{_datadir}/gtksourceview-2.0
%{_datadir}/qtvcp
%{_datadir}/icons/hicolor/*/*
%{_mandir}/man?/*

%files doc
%{_docdir}/%{name}

%files -n tcl-%{name}
%{tcl_sitearch}/%{name}%{version}

%files -n python-%{name}
%{python3_sitelib}/*

%files devel
%{_includedir}/linuxcnc
%{_libdir}/liblinuxcnc.a

%changelog
* Tue Sep 1 2020 spike <spike@fedoraproject.org> 2.9.0-2.20200901giteac9994
- Adjusted libdir file targets
- Added AutoReq: no to base package
- Updated to lastest git common on upstream master branch 


* Tue Sep 1 2020 spike <spike@fedoraproject.org> 2.9.0-2.20200901giteac9994
- Updated to lastest git common on upstream master branch 

* Mon Jun 15 2020 spike <spike@fedoraproject.org> 2.9.0-1.20200615gitcda96a4
- Updated to lastest git common on upstream master branch

* Sun Feb 23 2020 spike <spike@fedoraproject.org> 2.7.15-1
- Updated to new upstream release 2.7.15
- Updated BuildRequires
- Added 'AutoReq: no' to python-linuxcnc
- Changed AutoReqProv to AutoReq
- Fixed python2 related rpm macros

* Sun Feb 23 2020 spike <spike@fedoraproject.org> 2.7.14-4
- Added pygtk2 to Requires for Fedora 31+

* Mon May 20 2019 spike <spike@fedoraproject.org> 2.7.14-3
- Fixed ambiguous shebangs for Fedora 30+
- Added python-Yapps and python2-gobject to BuildRequires
- Dropped support for Fedora 28 and older

* Sat Feb 2 2019 spike <spike@fedoraproject.org> 2.7.14-2
- Updated build requirements for fedora 29+

* Tue Jun 19 2018 spike <spike@fedoraproject.org> 2.7.14-1
- Updated to new upstream release 2.7.14

* Tue May 15 2018 spike <spike@fedoraproject.org> 2.7.13-2
- Added conditional build requirement for boost-python to build on rawhide

* Wed May 9 2018 spike <spike@fedoraproject.org> 2.7.13-1
- Updated to new upstream release 2.7.12

* Fri May 4 2018 spike <spike@fedoraproject.org> 2.7.12-2
- Building against libtirpc to be compatible with Fedora 28

* Fri Jan 26 2018 spike <spike@fedoraproject.org> 2.7.12-1
- Updated to new upstream release 2.7.12

* Fri Sep 1 2017 spike <spike@fedoraproject.org> 2.7.11-5
- Added dependencies for python2-tkinter, boost-python and tkimg

* Fri Sep 1 2017 spike <spike@fedoraproject.org> 2.7.11-4
- Added bwidget dependency

* Fri Aug 25 2017 spike <spike@fedoraproject.org> 2.7.11-3
- Minor spec file updates

* Fri Aug 25 2017 spike <spike@fedoraproject.org> 2.7.11-2
- Updated to build on Fedora 26
