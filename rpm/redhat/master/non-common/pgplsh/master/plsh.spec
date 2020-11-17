%global sname plsh

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20200522
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch1:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/petere/plsh
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.20200522-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
PL/sh is a procedural language handler for PostgreSQL that
allows you to write stored procedures in a shell of your choice.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/%{sname}.so
%doc NEWS COPYING README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/share/extension/%{sname}--1--2.sql
%{pginstdir}/share/extension/%{sname}--2.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200522-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200522-1
- Update to 1.20200522

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Sun Jan 20 2019 Devrim Gündüz <devrim@gunduz.org> - 1.20171014-1.2
- Fix PostgreSQL 11 builds

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.20171014-1.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 1.20171014
- Update to 1.20171014

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20130823-2
- Cosmetic cleanup
- Use more macros for unified spec file

* Mon Mar 17 2014 - Devrim Gündüz <devrim@gunduz.org> 1.20130823-1
- Update to 1.20130823
- Update download URL

* Tue Nov 27 2012 - Devrim Gündüz <devrim@gunduz.org> 1.20121018-1
- Rewrite the spec file based on the new version, and update
  to 1.20121018

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for Fedora
