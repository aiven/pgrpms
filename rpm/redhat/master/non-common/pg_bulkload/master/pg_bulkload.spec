%global debug_package %{nil}

%global sname pg_bulkload
# Please note underscores -- this reflects the tarball name:
%global pgbulkloadpackagever 3_1_16

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	3.1.16
Release:	1%{?dist}
URL:		https://github.com/ossc-db/%{sname}
Source0:	https://github.com/ossc-db/%{sname}/archive/VERSION%{pgbulkloadpackagever}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel, pam-devel
BuildRequires:	libsepol-devel, readline-devel, krb5-devel
Requires:	postgresql%{pgmajorversion}-server %{sname}%{pgmajorversion}-client
Obsoletes:	%{sname} <= %{version}-1

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%package client
Summary:	High speed data loading utility for PostgreSQL
Requires:	postgresql%{pgmajorversion}-libs

%description client
pg_bulkload client subpackage provides client-only tools.

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}
%patch0 -p0

%build
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/pg_bulkload.so
%{pginstdir}/lib/pg_timestamp.so
%{pginstdir}/share/contrib/pg_timestamp.sql
%{pginstdir}/share/contrib/uninstall_pg_timestamp.sql
%{pginstdir}/share/extension/pg_bulkload*.sql
%{pginstdir}/share/extension/pg_bulkload.control
%{pginstdir}/share/extension/uninstall_pg_bulkload.sql
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp/*.bc
  %endif
 %endif
%endif

%files client
%defattr(-,root,root)
%{pginstdir}/bin/pg_bulkload
%{pginstdir}/bin/postgresql

%changelog
* Mon Jan 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.16-1
- Update to 3.1.16

* Tue Jan 22 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.15-1
- Update to 3.1.15

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.1.14-2.1
- Rebuild against PostgreSQL 11.0

* Sun Mar 4 2018 Devrim Gündüz <devrim@gunduz.org> 3.1.14-2
- Split client tools into a separate subpackage, per #3165

* Mon Nov 13 2017 Devrim Gündüz <devrim@gunduz.org> 3.1.14-1
- Update to 3.1.14

* Thu May 18 2017 Devrim Gündüz <devrim@gunduz.org> 3.1.13-1
- Update to 3.1.13

* Thu Sep 29 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.10-1
- Update to 3.1.10

* Thu Feb 11 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.9-1
- Update to 3.1.9

* Sun Jan 24 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.8-1
- Update to 3.1.8
- Update URL

* Thu May 29 2014 Devrim Gündüz <devrim@gunduz.org> 3.1.6-1
- Update to 3.1.6
- Simplify install section

* Fri Jan 22 2010 Devrim Gündüz <devrim@gunduz.org> 3.0a2-1
- Update to 3.0a2

* Fri Apr 18 2008 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PGDG Repository
