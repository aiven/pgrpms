%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname pg_bulkload

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	3.1.6
Release:	1%{?dist}
URL:		http://pgfoundry.org/projects/pgbulkload/
Source0:	http://pgfoundry.org/frs/download.php/3653/%{sname}-%{version}.tar.gz
Patch0:		pg_bulkload-makefile.patch
License:	BSD
Group:		Applications/Databases
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel, pam-devel
BuildRequires:	libsepol-devel, readline-devel, krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build

make USE_PGXS=1 %{?_smp_mflags}

%install

rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
#%doc README.pg_bulkload
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
* Thu May 29 2014 Devrim GUNDUZ <devrim@gunduz.org> 3.1.6-1
- Update to 3.1.6
- Simplify install section

* Fri Jan 22 2010 Devrim GUNDUZ <devrim@gunduz.org> 3.0a2-1
- Update to 3.0a2

* Fri Apr 18 2008 Devrim GUNDUZ <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PGDG Repository
