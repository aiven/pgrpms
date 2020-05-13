%global debug_package %{nil}
%global sname plpgsql_check

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.9.2
Release:	1%{?dist}
Summary:	Additional tools for PL/pgSQL functions validation

License:	BSD
URL:		https://github.com/okbob/%{sname}
Source0:	https://github.com/okbob/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
The plpgsql_check is PostgreSQL extension with functionality for direct
or indirect extra validation of functions in PL/pgSQL language. It verifies
a validity of SQL identifiers used in PL/pgSQL code. It also tries to identify
performance issues.

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
%{__make} USE_PGXS=1 DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
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
* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.2-1
- Update to 1.9.2

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0
- Switch to pgdg-srpm-macros

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.6-1
- Update to 1.7.6

* Thu Aug 15 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.4-1
- Update to 1.7.4

* Wed Jul 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.3-1
- Update to 1.7.3

* Fri Apr 26 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.1-1
- Update to 1.7.1

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 19 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Fri Sep 15 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1, per #2711

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.0.5

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Tue Jan 20 2015 - Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3

* Mon Aug 25 2014 - Pavel STEHULE <pavel.stehule@gmail.com> 0.9.2-1
- Initial packaging
