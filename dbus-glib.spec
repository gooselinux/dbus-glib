%define gettext_package dbus

%define expat_version           1.95.5
%define glib2_version           2.2.0
%define gtk2_version 2.4.0
%define dbus_version 0.90

Summary: GLib bindings for D-Bus
Name: dbus-glib
Version: 0.86
Release: 5%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus-glib
Source0: http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
License: AFL and GPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: chkconfig >= 1.3.26
BuildRequires: libtool
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: libxml2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext
BuildRequires: autoconf
# this patch requires autoreconf
BuildRequires: autoconf automake libtool gettext-devel gtk-doc

Patch0: Respect-property-access-flags-for-writing-allow-disa.patch
# Upstream http://cgit.freedesktop.org/dbus/dbus-glib/commit/?id=7f054d7bce4b2ea74e5268f2cf65c467773ee14f
Patch1: 0001-Fix-lookup-of-regular-properties-when-shadow-propert.patch

%description

D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%package devel
Summary: Libraries and headers for the D-Bus GLib bindings
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: glib2-devel
Requires: dbus-devel
Requires: pkgconfig
Obsoletes: dbus-devel < 0.90

%description devel

Headers and static libraries for the D-Bus GLib bindings

%if 0
%package gtk
Summary: GTK based tools
Group: Development/Tools
Requires: %name = %{version}-%{release}
Requires: gtk2 >= %{gtk_version}
%description gtk

D-Bus tools written using the gtk+ GUI libaries

%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
libtoolize --force --copy
autoreconf
%configure --disable-tests \
	--enable-verbose-mode=yes \
	--enable-asserts=yes \
	--disable-gtk-doc

#build with checks for right now but disable checks for final release
#%configure  --disable-tests --disable-verbose-mode --disable-asserts
make

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

%doc COPYING ChangeLog NEWS

%{_libdir}/*glib*.so.*
%{_bindir}/dbus-binding-tool

%files devel
%defattr(-,root,root)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/dbus-glib-1.pc
%{_includedir}/dbus-1.0/dbus/*
%{_datadir}/gtk-doc/html/dbus-glib
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
%{_libexecdir}/dbus-bash-completion-helper

%if 0
%files gtk
%defattr(-,root,root)

%{_bindir}/dbus-viewer

%endif

%changelog
* Wed Jul 14 2010 Colin Walters <walters@redhat.com> - 0.86-5
- Add patch from upstream to fix shadow properties
  Resolves: #609628

* Wed Apr 28 2010 Colin Walters <walters@redhat.com> - 0.86-3
- Sync with F-13 (bugfix only release)
- Add patch to validate property access
  Resolves: #585396

* Thu Mar 18 2010 Colin Walters <walters@verbum.org> - 0.86-1
- New upstream
  Drop upstreamed patch

* Tue Mar 02 2010 Colin Walters <walters@verbum.org> - 0.84-3
- Revert previous broken patch for error names, add better fix

* Mon Feb 15 2010 Colin Walters <walters@verbum.org> - 0.84-2
- Add patch to avoid assertions when setting a GError that
  includes a '-' in the enumeration value.  Should fix #528897

* Wed Jan 27 2010 Colin Walters <walters@verbum.org> - 0.84-1
- New upstream
  Has introspect.xml internally, drop it from here

* Fri Jan 15 2010 Colin Walters <walters@verbum.org> - 0.82-3
- Add ListActivatableNames to dbus-bus-introspect.xml to help tracker build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Colin Walters <walters@verbum.org> - 0.82-1
- New upstream 0.82
- Remove mclasen accidental commit of CFLAGS="-O0 -g3"

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 0.80-3
- Minor directory ownership cleanup

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Colin Walters <walters@verbum.org> - 0.80-1
- New upstream release
- Adjust to new bash completion dir
- Includes patch noreply patch

* Wed Jan 07 2009 Colin Walters <walters@verbum.org> - 0.78-2
- Add patch to avoid sending reply to noreply messages; this avoids
  some spurious dbus denial logs during system startup from NM

* Thu Dec 04 2008 Colin Walters <walters@verbum.org> - 0.78-1
- New upstream release, drop upstreamed patches

* Tue Nov 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.76-4
- Avoid some spurious linkage

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> - 0.76-3
- Fix crashes when a tracked service restarts too quickly (fdo #18573)

* Thu Jul 31 2008 David Zeuthen <davidz@redhat.com> - 0.76-2
- Add bash completion for dbus-send(1)

* Thu Jun 05 2008 Colin Walters <walters@redhat.com> - 0.76-1
- New upstream 0.76
- Drop all upstreamed patches

* Tue May 27 2008 Dan Williams <dcbw@redhat.com> - 0.74-9
- Handle unknown object properties without asserting (fdo #16079)
- Handle GetAll() property names correctly (fdo #16114)
- Enable the freeze-abi patch
- Cherry-pick some fixes from upstream git

* Thu May  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.74-8
- Fix license field

* Tue Apr 15 2008 Colin Walters <walters@redhat.com> - 0.74-7
- Ensure ABI is frozen as it stands now

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-6
- Add another upstreamed patch for setting the default timeout
  on a proxy

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-5
- Add an already upstreamed patch to export the GetAll() method on
  the org.freedesktop.DBus.Properties interface

* Wed Mar 19 2008 Dan Williams <dcbw@redhat.com> - 0.74-4
- Ignore children of namespaced nodes too

* Tue Feb 12 2008 Dan Williams <dcbw@redhat.com> - 0.74-3
- Ignore namespaces in introspection XML

* Sun Nov 18 2007 Dan Williams <dcbw@redhat.com> - 0.74-2
- Actually apply the patch for fdo #12505

* Mon Oct 22 2007 Ray Strode <rstrode@redhat.com> - 0.74-1
- Update to 0.74

* Mon Sep 24 2007 Dan Williams <dcbw@redhat.com> - 0.73-4
- Dispatch NameOwnerChanged signals to proxies only once (fdo #12505)

* Sat Sep 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-3
- Rebuild against new expat

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-2
- Fix a bug in introspection support (#248150)

* Wed Apr  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-1
- Update to 0.73 (#233631)
- Drop upstreamed patches

* Tue Dec 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.71-4
- Add dbus-glib-0.70-use-default-threads.patch
- Partial fix to #219257

* Wed Nov 29 2006 David Zeuthen <davidz@redhat.com> - 0.71-3%{?dist}
- Add dbus-glib-0.70-fix-info-leak.patch
- Resolves: #216034

* Sun Nov  5 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-2
- Fix up Requires for the -devel package

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-1
- Update to 0.71

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-4
- remove improper obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Pregenerate the xml introspect file so you don't need dbus running during
  the build 

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial dbus-glib package
