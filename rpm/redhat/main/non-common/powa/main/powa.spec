%global sname powa

Summary:	PostgreSQL Workload Analyzer Meta Package
Name:		%{sname}_%{pgmajorversion}
Version:	4.2.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://powa.readthedocs.io/
Requires:	postgresql%{pgmajorversion}-contrib
Requires:	powa-archivist_%{pgmajorversion}	pg_qualstats_%{pgmajorversion}
Requires:	pg_stat_kcache_%{pgmajorversion} hypopg_%{pgmajorversion}

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your
PostgreSQL servers. It is similar to Oracle AWR or SQL Server MDW.

This is the meta package.

%prep

%build

%install

%files

%changelog
* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
