Summary:	C library for accessing the PostgreSQL parser outside of the server
Name:		libpg_query
Version:	2.1.0
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/pganalyze/%{name}
Source0:	https://github.com/pganalyze/libpg_query/archive/refs/tags/13-%{version}.tar.gz
Patch0:		libpg_query-makefile-rpm.patch

%description
This library uses the actual PostgreSQL server source to parse SQL queries and
return the internal PostgreSQL parse tree.

Note that this is mostly intended as a base library for pg_query (Ruby),
pg_query.go (Go), pgsql-parser (Node), psqlparse (Python) and pglast
(Python 3).

%prep
%setup -q -n %{name}-13-%{version}
%patch0 -p0

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
%{_libdir}/libpg_query.so
%{_libdir}/libpg_query.so.1302.1
%{_libdir}/libpg_query.so.1302.1.0

%changelog
* Fri Mar 11 2022 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
