%global sname pg_pathman

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Partitioning tool for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.12
Release:	2%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server python3-psycopg2

Obsoletes:	%{sname}%{pgmajorversion} < 1.5.11-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
The pg_pathman module provides optimized partitioning mechanism and functions
to manage partitions.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p  %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/compat/*.bc
  %endif
 %endif
%endif

%changelog
* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 1.5.12-2
- Remove pgxs patches, and export PATH instead.

* Mon Nov 9 2020 Devrim Gündüz <devrim@gunduz.org> 1.5.12-1
- Update to 1.5.12

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.5.11-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Aug 7 2020 Devrim Gündüz <devrim@gunduz.org> 1.5.11-2
- Add explicit dependency to the PY3 version of psycopg2, per
  Sergejs Žuromskis.

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> 1.5.11-1
- Update to 1.5.11

* Thu Jan 2 2020 Devrim Gündüz <devrim@gunduz.org> 1.5.10-1
- Update to 1.5.10

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed Jul 3 2019 Devrim Gündüz <devrim@gunduz.org> 1.5.8-1
- Update to 1.5.8

* Tue Oct 16 2018 Devrim Gündüz <devrim@gunduz.org> 1.5.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Oct 16 2018 - Devrim Gündüz <devrim@gunduz.org> 1.5.2-1
- Update to 1.5.2

* Tue Sep 25 2018 - Devrim Gündüz <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Mon Sep 24 2018 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Sat Jul 14 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.13-1
- Update to 1.4.13

* Mon May 14 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.12-1
- Update to 1.4.12

* Sun Apr 29 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.11-1
- Update to 1.4.11

* Sun Dec 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.9-1
- Update to 1.4.9

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.7-1
- Update to 1.4.7, per #2790

* Sun Sep 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.5-1
- Update to 1.4.5

* Thu Aug 24 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Update to 1.4.3

* Sun Jun 11 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4

* Sat May 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Wed Dec 21 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
