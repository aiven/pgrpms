%global sname	oracle_fdw
%global ofdwmajver 2
%global ofdwmidver 6
%global ofdwminver 0

# Override RPM dependency generation to filter out libclntsh.so.
# http://fedoraproject.org/wiki/PackagingDrafts/FilteringAutomaticDependencies
%global		_use_internal_dependency_generator 0
%global		__find_requires %{SOURCE1}

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

Summary:	A PostgreSQL Foreign Data Wrapper for Oracle.
Name:		%{sname}_%{pgmajorversion}
Version:	%{ofdwmajver}.%{ofdwmidver}.%{ofdwminver}
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		http://laurenz.github.io/%{sname}
Source0:	https://github.com/laurenz/%{sname}/archive/ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}.tar.gz
Source1:	%{sname}-filter-requires-libclntsh.sh
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.3.0-2

Requires:	postgresql%{pgmajorversion}-server
# Package builder needs to adjust this as needed.
BuildRequires:	oracle-instantclient-basic >= 21.11.0.0.0
BuildRequires:	oracle-instantclient-devel >= 21.11.0.0.0
Requires:	oracle-instantclient-basic >= 21.11.0.0.0

%description
Provides a Foreign Data Wrapper for easy and efficient read access from
PostgreSQL to Oracle databases, including pushdown of WHERE conditions and
required columns as well as comprehensive EXPLAIN support.

%prep
%setup -q -n %{sname}-ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}

%build

PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if %runselftest
%{__make} installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres PGPORT=5495
%endif

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README.%{sname}

%changelog
* Mon Sep 11 2023 Devrim Gündüz <devrim@gunduz.org> 2.6.0-1PGDG
- Update to 2.6.0
- Add PGDG branding
- Build against OIC 21.11.0.0.0

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.0-3
- Rebuild against OIC 21.10

* Fri Feb 3 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.0-2
- Rebuild against OIC 21.9

* Fri Oct 28 2022 Devrim Gündüz <devrim@gunduz.org> 2.5.0-1
- Update to 2.5.0
- Rebuild against OIC 21.8

* Sat Sep 10 2022 Devrim Gündüz <devrim@gunduz.org> 2.4.0-3
- Rebuild against OIC 21.7
- Remove pgxs patches, and export PATH instead.

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> 2.2.0-2
- Update LLVM dependencies
- Switch to pgdg-srpm-macros

* Fri Oct 11 2019 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Fri Oct 5 2018 Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Tue Sep 19 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0
- Put check into conditional, and disable it by default.
- Update for new doc layout.

* Tue Feb 3 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Add a patch for PGXS compilation.
- Ran dos2unix against the spec file, to fix build issues.

* Thu Dec 26 2013 Devrim Gündüz <devrim@gunduz.org> 0.9.10-1
- Update to 0.9.10-1

* Mon Oct 8 2012 David E. Wheeler <david.wheeler@iovation.com> 0.9.7-1
- Initial RPM
 
