%define name rarian
%define version 0.5.8
%define release %mkrel 1
%define major 0
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name
%define xmlcatalog      %{_sysconfdir}/xml/catalog

Summary: Rarian is a cataloging system for documentation on open systems
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: scrollkeeper-omf.dtd
# gw https://bugs.freedesktop.org/show_bug.cgi?id=11779
Patch0: rarian-0.5.4-mv.patch
Patch1:	rarian-0.5.8-lzma-support.patch
License: GPL
Group: Publishing
Url: http://www.gnome.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides: scrollkeeper = %version-%release
Obsoletes: scrollkeeper
Requires(post): libxml2-utils
Requires(preun): libxml2-utils


%description
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay (as
far as my testing indicates)

%package -n %libname
Group:System/Libraries
Summary: Rarian cataloging system library

%description -n %libname
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay (as
far as my testing indicates)

%package -n %libnamedev
Group: Development/C
Summary: Rarian cataloging system - development files
Requires: %libname = %version
Provides: %name-devel = %version-%release
Provides: lib%name-devel = %version-%release
Provides: scrollkeeper-devel = %version-%release

%description -n %libnamedev
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay (as
far as my testing indicates)

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure2_5x --disable-skdb-update --localstatedir=/var
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std localstatedir=%buildroot/var
mkdir -p %buildroot/var/lib/rarian
touch %buildroot/var/lib/rarian/rarian-update-mtimes
install -D -m 644 %SOURCE1 %buildroot%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd

%clean
rm -rf $RPM_BUILD_ROOT

%post
  if [ "$1" = "1" ]; then
%_bindir/rarian-sk-update
%{_bindir}/xmlcatalog --noout --add "public" \
        "-//OMF//DTD Scrollkeeper OMF Variant V1.0//EN" \
        "%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %xmlcatalog
fi
%_bindir/rarian-sk-rebuild > /dev/null || true

%preun
if [ "$1" = "0" -a -f %xmlcatalog -a -x %{_bindir}/xmlcatalog ] ; then
  %{_bindir}/xmlcatalog --noout --del \
	"%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %xmlcatalog
fi

%postun
if [ "$1" = "0" ]; then
  # rarian is being removed, not upgraded.  
  rm -f %_datadir/help/*.document
fi

%triggerpostun -- scrollkeeper < 0.5.6-2mdv
%{_bindir}/xmlcatalog --noout --add "public" \
        "-//OMF//DTD Scrollkeeper OMF Variant V1.0//EN" \
        "%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %xmlcatalog


%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README NEWS 
%_bindir/rarian*
%_bindir/scrollkeeper*
%dir %_datadir/help/
%_datadir/help/rarian.document
%_datadir/librarian
%dir %{_datadir}/xml/scrollkeeper/
%dir %{_datadir}/xml/scrollkeeper/dtds/
%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd
%dir /var/lib/rarian
%ghost /var/lib/rarian/rarian-update-mtimes

%files -n %libname
%defattr(-,root,root)
%_libdir/librarian.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%doc ChangeLog TODO
%_libdir/librarian.so
%_libdir/librarian.a
%_libdir/librarian.la
%_includedir/rarian
%_libdir/pkgconfig/rarian.pc
