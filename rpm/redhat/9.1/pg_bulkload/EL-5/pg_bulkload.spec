%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pg_bulkload
# Please note underscores -- this reflects the tarball name:
%global pgbulkloadpackagever 3_1_10

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	3.1.10
Release:	1%{?dist}
URL:		https://github.com/ossc-db/pg_bulkload
Source0:	https://github.com/ossc-db/pg_bulkload/archive/VERSION%{pgbulkloadpackagever}.tar.gz
Patch0:		pg_bulkload-makefile.patch
License:	BSD
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel, pam-devel
BuildRequires:	libsepol-devel, readline-devel, krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc doc/
%{pginstdir}/bin/pg_bulkload
%{pginstdir}/bin/postgresql
%{pginstdir}/lib/pg_bulkload.so
%{pginstdir}/lib/pg_timestamp.so
%{pginstdir}/share/contrib/pg_timestamp.sql
%{pginstdir}/share/contrib/uninstall_pg_timestamp.sql
%{pginstdir}/share/extension/pg_bulkload*.sql
%{pginstdir}/share/extension/pg_bulkload.control
%{pginstdir}/share/extension/uninstall_pg_bulkload.sql

%changelog
* Thu Sep 29 2016 Devrim GUNDUZ <devrim@gunduz.org> 3.1.10-1
- Update to 3.1.10

* Thu Feb 11 2016 Devrim GUNDUZ <devrim@gunduz.org> 3.1.9-1
- Update to 3.1.9

* Sun Jan 24 2016 Devrim GUNDUZ <devrim@gunduz.org> 3.1.8-1
- Update to 3.1.8
- Update URL

* Thu May 29 2014 Devrim GUNDUZ <devrim@gunduz.org> 3.1.6-1
- Update to 3.1.6
- Simplify install section

* Fri Jan 22 2010 Devrim GUNDUZ <devrim@gunduz.org> 3.0a2-1
- Update to 3.0a2

* Fri Apr 18 2008 Devrim GUNDUZ <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PGDG Repository
