%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define xmlcatalog %{_sysconfdir}/xml/catalog

Summary:	Cataloging system for documentation on open systems
Name:		rarian
Version:	0.8.1
Release:	17
License:	GPLv2+
Group:		Publishing
Url:		http://rarian.freedesktop.org/
Source0:	http://rarian.freedesktop.org/Releases/%{name}-%{version}.tar.bz2
Source1:	scrollkeeper-omf.dtd
Source2:	rarian.rpmlintrc
# gw https://bugs.freedesktop.org/show_bug.cgi?id=11779
Patch0:		rarian-0.5.4-mv.patch
Patch1:		rarian-0.8.1-xz-support.patch
Requires(post):	libxml2-utils sgml-common util-linux-ng
Requires(preun):	libxml2-utils sgml-common
%rename		scrollkeeper

%description
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Rarian cataloging system library

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	%{devname}
Group:		Development/C
Summary:	Rarian cataloging system - development files
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-skdb-update \
	--localstatedir=/var
%make

%install
%makeinstall_std localstatedir=%{buildroot}/var
mkdir -p %{buildroot}/var/lib/rarian
touch %{buildroot}/var/lib/rarian/rarian-update-mtimes
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd

%post
  if [ "$1" = "1" ]; then
%{_bindir}/rarian-sk-update
%{_bindir}/xmlcatalog --noout --add "public" \
        "-//OMF//DTD Scrollkeeper OMF Variant V1.0//EN" \
        "%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %{xmlcatalog}
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
        "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/" \
        "file:///usr/share/xml/scrollkeeper/dtds/" %{xmlcatalog}
fi
%{_bindir}/rarian-sk-rebuild > /dev/null || true

%preun
if [ "$1" = "0" -a -f %{xmlcatalog} -a -x %{_bindir}/xmlcatalog ] ; then
  %{_bindir}/xmlcatalog --noout --del \
	"%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %{xmlcatalog}
fi

%postun
if [ "$1" = "0" ]; then
  # rarian is being removed, not upgraded.  
  rm -f %{_datadir}/help/*.document
fi

%triggerpostun -- scrollkeeper < 0.5.6-2mdv
%{_bindir}/xmlcatalog --noout --add "public" \
        "-//OMF//DTD Scrollkeeper OMF Variant V1.0//EN" \
        "%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" %{xmlcatalog}

%triggerin -- %{_datadir}/omf/*/*.omf
%{_bindir}/scrollkeeper-update -q

%triggerpostun -- %{_datadir}/omf/*/*.omf
%{_bindir}/scrollkeeper-update -q

%files
%doc README NEWS 
%{_bindir}/rarian*
%{_bindir}/scrollkeeper*
%dir %{_datadir}/help/
%{_datadir}/help/rarian.document
%{_datadir}/librarian
%dir %{_datadir}/xml/scrollkeeper/
%dir %{_datadir}/xml/scrollkeeper/dtds/
%{_datadir}/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd
%dir /var/lib/rarian
%ghost /var/lib/rarian/rarian-update-mtimes

%files -n %{libname}
%{_libdir}/librarian.so.%{major}*

%files -n %{devname}
%doc ChangeLog TODO
%{_libdir}/librarian.so
%{_includedir}/rarian
%{_libdir}/pkgconfig/rarian.pc

