%undefine _package_note_file
%global sname pgcopydb

Summary:	Automate pg_dump | pg_restore between two running Postgres servers
Name:		%{sname}_%{pgmajorversion}
Version:	0.9
Release:	2%{?dist}
License:	PostgreSQL
Source0:	https://github.com/dimitri/pgcopydb/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/dimitri/pgcopydb

BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel
BuildRequires:	pgdg-srpm-macros krb5-devel, bison, flex
Requires:	postgresql%{pgmajorversion}

%description
pgcopydb is a tool that automates running pg_dump | pg_restore between
two running Postgres servers. To make a copy of a database to another
server as quickly as possible, one would like to use the parallel
options of pg_dump and still be able to stream the data to as many
pg_restore jobs.
%prep
%setup -q -n %{sname}-%{version}

USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%{pginstdir}/bin/pgcopydb

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.9-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 - Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Initial packaging for the PostgreSQL RPM repository
