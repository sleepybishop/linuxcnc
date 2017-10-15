# quicker build with no docs
%global _without_docs 1

# pre-release settings
%global _pre      1 

Name:           linuxcnc
Version:        2.8.0
Release:        0%{?_pre:.%{_pre}}%{?dist}
Summary:        A software system for computer control of machine tools

License:        GPLv2
Group:          Applications/Engineering
URL:            http://www.linuxcnc.org
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gtk2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  bwidget
BuildRequires:  libXaw-devel
BuildRequires:  python-mtTkinter
BuildRequires:  boost-devel
BuildRequires:  pth-devel
BuildRequires:  libmodbus-devel
BuildRequires:  blt-devel
BuildRequires:  readline-devel
BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  python-lxml
BuildRequires:	libudev-devel
# for building docs
%if ! %{_without_docs}
BuildRequires:  lyx
BuildRequires:  source-highlight
BuildRequires:  ImageMagick
BuildRequires:  dvipng
BuildRequires:  dblatex
BuildRequires:  asciidoc >= 8.5
%endif
#

Requires:       bwidget
Requires:       blt
Requires:       tclx
Requires:       tkimg
Requires:       python-mtTkinter
Requires:       python-xlib
Requires:       pygtkglext
Requires:       boost-python
Requires:       python-pillow-tk
Requires:       gstreamer-python

#Requires:       kernel-rt

Autoreq: 0

%description

LinuxCNC (the Enhanced Machine Control) is a software system for
computer control of machine tools such as milling machines and lathes.

%package devel
Group: Development/Libraries
Summary: Devel package for %{name}
Requires: %{name} = %{version}

%description devel
Development headers and libs for the %{name} package

%package doc
Group:          Documentation
Summary:        Documentation for %{name}

%description doc

Documentation files for the %{name} package

%prep
%setup -q


%build
cd src
./autogen.sh
%configure \
%if ! 0%{_without_docs}
    --enable-build-documentation \
%endif
    --with-realtime=uspace \
    --without-libusb-1.0 \
    --with-tkConfig=%{_libdir}/tkConfig.sh \
    --with-tclConfig=%{_libdir}/tclConfig.sh \
    --enable-non-distributable=yes
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
cd src
make -e install DESTDIR=$RPM_BUILD_ROOT \
     DIR='install -d -m 0755' FILE='install -m 0644' \
     EXE='install -m 0755' SETUID='install -m 0755'
# put the docs in the right place
mv $RPM_BUILD_ROOT/usr/share/doc/linuxcnc \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# put X11 app-defaults where the rest of them live
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11 $RPM_BUILD_ROOT%{_datadir}/

# Set the module(s) to be executable, so that they will be stripped
# when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

# put tcltk libs in proper place
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/tcl8.6/
#mv $RPM_BUILD_ROOT%{_exec_prefix}/lib/tcltk/linuxcnc ${RPM_BUILD_ROOT}%{_libdir}/tcl8.6/linuxcnc
ln -s %{_exec_prefix}/lib/tcltk/linuxcnc ${RPM_BUILD_ROOT}%{_libdir}/tcl8.6/linuxcnc

%files
%defattr(-,root,root)
%{_sysconfdir}/linuxcnc
%{_sysconfdir}/init.d/realtime

%{_datadir}/X11/app-defaults/*
%attr(04755,-,-) %{_bindir}/rtapi_app
%attr(0755,-,-) %{_bindir}/5axisgui
%attr(0755,-,-) %{_bindir}/axis
%attr(0755,-,-) %{_bindir}/axis-remote
%attr(0755,-,-) %{_bindir}/classicladder
%attr(0755,-,-) %{_bindir}/debuglevel
%attr(0755,-,-) %{_bindir}/elbpcom
%attr(0755,-,-) %{_bindir}/genserkins
%attr(0755,-,-) %{_bindir}/gladevcp
%attr(0755,-,-) %{_bindir}/gladevcp_demo
%attr(0755,-,-) %{_bindir}/gmoccapy
%attr(0755,-,-) %{_bindir}/gremlin_view
%attr(0755,-,-) %{_bindir}/gs2_vfd
%attr(0755,-,-) %{_bindir}/gscreen
%attr(0755,-,-) %{_bindir}/hal-histogram
%attr(0755,-,-) %{_bindir}/hal_input
%attr(0755,-,-) %{_bindir}/hal_manualtoolchange
%attr(0755,-,-) %{_bindir}/halcmd
%attr(0755,-,-) %{_bindir}/halcompile
%attr(0755,-,-) %{_bindir}/halmeter
%attr(0755,-,-) %{_bindir}/halrmt
%attr(0755,-,-) %{_bindir}/halrun
%attr(0755,-,-) %{_bindir}/halsampler
%attr(0755,-,-) %{_bindir}/halscope
%attr(0755,-,-) %{_bindir}/halshow
%attr(0755,-,-) %{_bindir}/halstreamer
%attr(0755,-,-) %{_bindir}/haltcl
%attr(0755,-,-) %{_bindir}/halui
%attr(0755,-,-) %{_bindir}/hbmgui
%attr(0755,-,-) %{_bindir}/hexagui
%attr(0755,-,-) %{_bindir}/hy_vfd
%attr(0755,-,-) %{_bindir}/image-to-gcode
%attr(0755,-,-) %{_bindir}/inivar
%attr(0755,-,-) %{_bindir}/io
%attr(0755,-,-) %{_bindir}/iov2
%attr(0755,-,-) %{_bindir}/keystick
%attr(0755,-,-) %{_bindir}/maho600gui
%attr(0755,-,-) %{_bindir}/max5gui
%attr(0755,-,-) %{_bindir}/mb2hal
%attr(0755,-,-) %{_bindir}/mdi
%attr(0755,-,-) %{_bindir}/milltask
%attr(0755,-,-) %{_bindir}/monitor-xhc-hb04
%attr(0755,-,-) %{_bindir}/motion-logger
%attr(0755,-,-) %{_bindir}/moveoff_gui
%attr(0755,-,-) %{_bindir}/ngcgui
%attr(0755,-,-) %{_bindir}/pncconf
%attr(0755,-,-) %{_bindir}/puma560gui
%attr(0755,-,-) %{_bindir}/pumagui
%attr(0755,-,-) %{_bindir}/pyngcgui
%attr(0755,-,-) %{_bindir}/pyvcp
%attr(0755,-,-) %{_bindir}/pyvcp_demo
%attr(0755,-,-) %{_bindir}/rs274
%attr(0755,-,-) %{_bindir}/scaragui
%attr(0755,-,-) %{_bindir}/schedrmt
%attr(0755,-,-) %{_bindir}/shuttlexpress
%attr(0755,-,-) %{_bindir}/sim_pin
%attr(0755,-,-) %{_bindir}/simulate_probe
%attr(0755,-,-) %{_bindir}/stepconf
%attr(0755,-,-) %{_bindir}/tooledit
%attr(0755,-,-) %{_bindir}/touchy
%attr(0755,-,-) %{_bindir}/vfdb_vfd
%attr(0755,-,-) %{_bindir}/vfs11_vfd
%attr(0755,-,-) %{_bindir}/wj200_vfd
%attr(0755,-,-) %{_bindir}/xhc-hb04-accels
%attr(0755,-,-) %{_bindir}/xlinuxcnc
%attr(0755,-,-) %{_bindir}/linuxcnc
%attr(0755,-,-) %{_bindir}/linuxcnc[a-z]*
%attr(0755,-,-) %{_bindir}/linuxcnc_info
%attr(0755,-,-) %{_bindir}/linuxcnc_var
%attr(0755,-,-) %{_bindir}/latency*
%attr(0755,-,-) %{_bindir}/hy_gt_vfd
%attr(0755,-,-) %{_bindir}/mitsub_vfd

%{python_sitelib}/*
%{_exec_prefix}/lib/tcltk/*
%ghost %{_libdir}/tcl8.6/linuxcnc

#%{_libdir}/*.so*
%{_libdir}/libcanterp.so
%{_libdir}/libcanterp.so.0
%{_libdir}/liblinuxcnchal.so
%{_libdir}/liblinuxcnchal.so.0
%{_libdir}/liblinuxcncini.so
%{_libdir}/liblinuxcncini.so.0
%{_libdir}/libnml.so
%{_libdir}/libnml.so.0
%{_libdir}/libposemath.so
%{_libdir}/libposemath.so.0
%{_libdir}/libpyplugin.so.0
%{_libdir}/librs274.so
%{_libdir}/librs274.so.0

%attr(0775,-,-) /usr/lib/linuxcnc/modules

%{_datadir}/axis
%{_datadir}/gmoccapy
%{_datadir}/glade3
%{_datadir}/gtksourceview-2.0
%{_datadir}/linuxcnc
%{_datadir}/gscreen
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/linuxcnc.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/linuxcnc.mo
%lang(fi) %{_datadir}/locale/fi/LC_MESSAGES/linuxcnc.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/linuxcnc.mo
%lang(hu) %{_datadir}/locale/hu/LC_MESSAGES/linuxcnc.mo
%lang(it) %{_datadir}/locale/it/LC_MESSAGES/linuxcnc.mo
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/linuxcnc.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/linuxcnc.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/linuxcnc.mo
%lang(ro) %{_datadir}/locale/ro/LC_MESSAGES/linuxcnc.mo
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/linuxcnc.mo
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/linuxcnc.mo
%lang(sr) %{_datadir}/locale/sr/LC_MESSAGES/linuxcnc.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/linuxcnc.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/linuxcnc.mo
%lang(zh_HK) %{_datadir}/locale/zh_HK/LC_MESSAGES/linuxcnc.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/linuxcnc.mo

%lang(de) %{_datadir}/locale/de/LC_MESSAGES/gmoccapy.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/gmoccapy.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/gmoccapy.mo
%lang(hu) %{_datadir}/locale/hu/LC_MESSAGES/gmoccapy.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/gmoccapy.mo
%lang(sr) %{_datadir}/locale/sr/LC_MESSAGES/gmoccapy.mo

%doc %{_mandir}/man[19]/*

%files devel
%defattr(-,root,root)
%{_includedir}/linuxcnc
%{_libdir}/liblinuxcnc.a
%doc %{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

%changelog
* Sat Oct 14 2017 Joseph Calderon <@> - 2.8.0~pre1
- Update to 2.8.0

* Fri Feb  5 2016 Joseph Calderon <@> - 2.7.3-1
- Update to 2.7.3

* Fri Oct  2 2015 Joseph Calderon <@> - 2.7.0-1
- Update to 2.7.0 

* Thu Sep  5 2013 John Morris <john@zultron.com> - 2.6.0-0.5.ubc3
- Update to 2.6.0-20130905git05ed2b1
- Refactor for Universal Build (universal-build-candidate-3)
- Build all flavors by default, with one kernel source per kthread flavor
- Break out flavor binaries into subpackages
- Disable RTAI build until we have RTAI packages
- Refactor macro system

* Mon Nov 12 2012 John Morris <john@zultron.com> - 2.6.0-0.4.pre0
- Update to 2.6.0-20121112gite024e61
-   Fix for Xenomai recommended kernel option
- Add preempt-rt support
- Generalize kernel package/version logic for various threads systems
  - Each thread system-specific section defines some config variables
  - Resulting logic is much simpler and easier to read
- Fix incorrect %defattr statements
- Bump xenomai kversion release
- Add thread system info in release tag
- Base kernel package version on -devel pkg, not kernel package
- Remove BR: kernel; should only need kernel-devel

* Fri Nov  9 2012 John Morris <john@zultron.com> - 2.6.0-0.3.pre0
- Update to 2.6.0-20121109git894f2cf
-   Fixes to compiler math options for xenomai
-   Fixes to kernel module symbol sharing
- Enable verbose builds
- Option to disable building docs for a quick build
- linuxcnc-module-helper setuid root
- rpmlint cleanups:  tabs, perms

* Sun May  6 2012  <john@zultron.com> - 2.6.0-0.1.pre0
- Updated to newest git:
  - Forward-port of Michael Buesch's patches
  - Fixes to the hal stacksize, no more crash!
  - Install shared libs mode 0755 for /usr/lib/rpm/rpmdeps

* Wed Apr 25 2012  <john@zultron.com> - 2.5.0.1-1
- Initial RPM version
