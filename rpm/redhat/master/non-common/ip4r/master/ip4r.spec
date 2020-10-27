%global sname ip4r

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Name:		%{sname}_%{pgmajorversion}
Summary:	IPv4/v6 and IPv4/v6 range index type for PostgreSQL
Version:	2.4.1
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/RhodiumToad/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/RhodiumToad/ip4r
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Provides:	postgresql-ip4r
Obsoletes:	%{sname}%{pgmajorversion} <= 2.4.1-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
ip4, ip4r, ip6, ip6r, ipaddress and iprange are types that contain a single
IPv4/IPv6 address and a range of IPv4/IPv6 addresses respectively. They can
be used as a more flexible, indexable version of the cidr type.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%{__rm} -f %{buildroot}%{pginstdir}/include/server/extension/ip4r/ipr.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README.ip4r
%{pginstdir}/lib/ip4r.so
%{pginstdir}/share/extension/ip4r*
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed May 22 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4-1
- Update to 2.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Jun 11 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Wed Apr 26 2017 Devrim Gündüz <devrim@gunduz.org> - 2.2-1
- Update to 2.2

* Sun Sep 18 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Update to 2.1

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Nov 9 2015 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-2
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Jun 11 2014 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2
- Update summary and description

* Sun Sep 15 2013 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0, using the "extension" tarball.

* Thu Mar 08 2012 Devrim Gündüz <devrim@gunduz.org> - 1.05-3
- Provide postgresql-ip4r, to match the package name in EPEL.

* Tue Oct 12 2010 - Devrim Gündüz <devrim@gunduz.org> 1.05-2
- Apply 9.0 specific changes to spec file.

* Wed Apr 21 2010 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Mon Sep 7 2009 - Devrim Gündüz <devrim@gunduz.org> 1.04-1
- Update to 1.04

* Fri Feb 1 2008 - Devrim Gündüz <devrim@gunduz.org> 1.03-1
- Update to 1.03

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 1.02-1
- Update to 1.02

* Mon Jul 9 2007 - Devrim Gündüz <devrim@gunduz.org> 1.01-2
- Removed unneeded ldconfig calls, per bz review #246747

* Wed Jul 4 2007 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial RPM packaging for Fedora
