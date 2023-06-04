Summary:	C library for accessing the PostgreSQL parser outside of the server
Name:		libpg_query
Version:	4.2.1
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/pganalyze/%{name}
Source0:	https://github.com/pganalyze/libpg_query/archive/refs/tags/15-%{version}.tar.gz
Patch0:		libpg_query-makefile-rpm.patch

%description
This library uses the actual PostgreSQL server source to parse SQL queries and
return the internal PostgreSQL parse tree.

Note that this is mostly intended as a base library for pg_query (Ruby),
pg_query.go (Go), pgsql-parser (Node), psqlparse (Python) and pglast
(Python 3).

%prep
%setup -q -n %{name}-15-%{version}
%patch -P 0 -p0

%build

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_includedir}/pg_query.h
%{_includedir}/pg_query/pg_query.proto
%{_libdir}/libpg_query.a
%{_libdir}/libpg_query.so*

%changelog
* Sun Jun 4 2023 - Devrim Gündüz <devrim@gunduz.org> 4.2.1-1
- Update to 4.2.1

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Apr 10 2023 - Devrim Gündüz <devrim@gunduz.org> 4.2.0-1
- Update to 4.2.0

* Fri Mar 11 2022 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
