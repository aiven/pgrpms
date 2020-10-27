%global sname orafce
%global orafcemajver 3
%global orafcemidver 13
%global orafceminver 4

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{orafcemajver}.%{orafcemidver}.%{orafceminver}
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/orafce/orafce

BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel
BuildRequires:	pgdg-srpm-macros krb5-devel, bison, flex
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} 3.13.4-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
The goal of this project is implementation some functions from Oracle database.
Some date functions (next_day, last_day, trunc, round, ...) are implemented
now. Functionality was verified on Oracle 10g and module is useful
for production work.

%prep
%setup -q -n %{sname}-VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/COPYRIGHT.orafce
%doc %{pginstdir}/doc/extension/INSTALL.orafce
%doc %{pginstdir}/doc/extension/README.asciidoc
%{pginstdir}/lib/orafce.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/orafce--*.sql
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
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 3.13.4-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> 3.13.4-1
- Update to 3.13.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> 3.11.1-1
- Update to 3.11.1

* Tue Feb 25 2020 Devrim Gündüz <devrim@gunduz.org> 3.9.0-1
- Update to 3.9.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Fri May 24 2019 Devrim Gündüz <devrim@gunduz.org> 3.8.0-1
- Update to 3.8.0

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> 3.7.2-1
- Update to 3.7.2

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Sat Feb 17 2018 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1
- Update to 3.6.1, per #3131
- Remove patch1, not needed anymore.

* Thu Oct 19 2017 - Devrim Gündüz <devrim@gunduz.org> 3.6.0-1
- Update to 3.6.0, per #2812

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 3.4.0-1
- Update to 3.4.0, per #2343.
- Add support for Power RPMs.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1

* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Fri Feb 19 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 3.1.2-1
- Update to 3.1.2

* Tue Jan 20 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.14-1
- Update to 3.0.14

* Wed Oct 22 2014 - Devrim Gündüz <devrim@gunduz.org> 3.0.7-1
- Update to 3.0.7

* Thu Sep 13 2012 - Devrim Gündüz <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Fri Oct 2 2009 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Remove patch0, it is in upstream now.
- Apply some 3.0 fixes to spec.

* Wed Aug 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.3-2
- Spec file fixes, per bz review #251805

* Mon Jan 14 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Fri Aug 10 2007 - Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial packaging
