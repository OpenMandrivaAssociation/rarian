%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define xmlcatalog      %{_sysconfdir}/xml/catalog

Summary:	Cataloging system for documentation on open systems
Name:		rarian
Version:	0.8.1
Release:	13
License:	GPLv2+
Group:		Publishing
Url:		http://rarian.freedesktop.org/
Source0:	http://rarian.freedesktop.org/Releases/%{name}-%{version}.tar.bz2
Source1:	scrollkeeper-omf.dtd
# gw https://bugs.freedesktop.org/show_bug.cgi?id=11779
Patch0:		rarian-0.5.4-mv.patch
Patch1:		rarian-0.8.1-xz-support.patch

Requires(post):	libxml2-utils sgml-common util-linux-ng
Requires(preun): libxml2-utils sgml-common
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
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay.

%package -n	%{develname}
Group:		Development/C
Summary:	Rarian cataloging system - development files
Requires:	%{libname} = %version
Provides:	%{name}-devel = %version-%release

%description -n	%{develname}
Rarian is a cataloging system for the installed documentation.

Rarian is designed to be a replacement for scrollkeeper.  It is
currently undergoing heavy development.  As of writing, rarian can be
installed in place of scrollkeeper and everything will work okay.

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

%files -n %{develname}
%doc ChangeLog TODO
%{_libdir}/librarian.so
%{_includedir}/rarian
%{_libdir}/pkgconfig/rarian.pc



%changelog
* Mon Apr 23 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.8.1-11
+ Revision: 793045
- rebuild
- cleaned up spec

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-10
+ Revision: 669408
- mass rebuild

* Sat Feb 26 2011 Götz Waschk <waschk@mandriva.org> 0.8.1-9
+ Revision: 640157
- fix xml catalog for new gtk-doc

* Sun Feb 13 2011 Funda Wang <fwang@mandriva.org> 0.8.1-8
+ Revision: 637583
- correctly match real omf files

* Sat Feb 12 2011 Götz Waschk <waschk@mandriva.org> 0.8.1-7
+ Revision: 637362
- replace rpm filetrigger script by rpm5 version

* Sun Oct 24 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.1-6mdv2011.0
+ Revision: 587817
- add xz support (P1)
- remove old ldconfig scriptlet for ancient releases
- cosmetics

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-5mdv2010.1
+ Revision: 523891
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.8.1-4mdv2010.0
+ Revision: 426875
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.8.1-3mdv2009.1
+ Revision: 351580
- rebuild

* Thu Sep 11 2008 Thierry Vignaud <tv@mandriva.org> 0.8.1-2mdv2009.0
+ Revision: 283750
- fix description

* Mon Sep 01 2008 Götz Waschk <waschk@mandriva.org> 0.8.1-1mdv2009.0
+ Revision: 278578
- new version

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.8.0-3mdv2009.0
+ Revision: 265616
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Pixel <pixel@mandriva.com> 0.8.0-2mdv2009.0
+ Revision: 217385
- add rpm filetrigger running scrollkeeper-update when rpm install/remove omf files
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Mar 09 2008 Götz Waschk <waschk@mandriva.org> 0.8.0-1mdv2008.1
+ Revision: 183052
- new version

* Sat Mar 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.1-4mdv2008.1
+ Revision: 177135
- requires(post) util-linux-ng, not getopt (there is no package called getopt, the getopt binary is in util-linux-ng)

* Sat Mar 01 2008 Olivier Blin <blino@mandriva.org> 0.7.1-3mdv2008.1
+ Revision: 176989
- require getopt in post (for rarian-sk-update)
- require sgml-common in post/preun (for /etc/xml/catalog)

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.7.1-2mdv2008.1
+ Revision: 171076
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

  + Funda Wang <fwang@mandriva.org>
    - clearify the SOURCE and URL

* Tue Jan 08 2008 Götz Waschk <waschk@mandriva.org> 0.7.1-1mdv2008.1
+ Revision: 146375
- new version
- drop patch 1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 27 2007 Götz Waschk <waschk@mandriva.org> 0.7.0-1mdv2008.1
+ Revision: 113305
- new version

* Thu Nov 15 2007 Frederic Crozat <fcrozat@mandriva.com> 0.6.0-2mdv2008.1
+ Revision: 108915
- Update patch1 for upstream submittion (fd.o bug #13255)
- Add comments to specfile and backup extension to patches

* Wed Sep 12 2007 Götz Waschk <waschk@mandriva.org> 0.6.0-1mdv2008.0
+ Revision: 84769
- new version

* Tue Aug 21 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.5.8-2mdv2008.0
+ Revision: 68289
- add lzma support P1

* Tue Aug 14 2007 Götz Waschk <waschk@mandriva.org> 0.5.8-1mdv2008.0
+ Revision: 63137
- new version
- drop patch 1

* Wed Aug 08 2007 Götz Waschk <waschk@mandriva.org> 0.5.6-3mdv2008.0
+ Revision: 60087
- fix a crash

* Wed Aug 01 2007 Götz Waschk <waschk@mandriva.org> 0.5.6-2mdv2008.0
+ Revision: 57402
- add scrollkeeper omf DTD

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.6-1mdv2008.0
+ Revision: 57222
- new version

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-5mdv2008.0
+ Revision: 57106
- fix error on uninstallation
- fix postun again

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-4mdv2008.0
+ Revision: 57024
- fix summary
- fix postun script
- handle generated file in var as ghost file

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-3mdv2008.0
+ Revision: 57000
- fix localstatedir

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-2mdv2008.0
+ Revision: 56982
- fix rarian-sk-rebuild call in the post script

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-1mdv2008.0
+ Revision: 56965
- Import rarian



* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.5.4-1mdv2008.0
- initial package
