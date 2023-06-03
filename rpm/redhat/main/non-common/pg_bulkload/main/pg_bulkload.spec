%global	debug_package %{nil}
%global	pgbulkloadpackagever 3_1_20

%global sname pg_bulkload

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.1.20
Release:	1%{?dist}.1
URL:		https://github.com/ossc-db/%{sname}
Source0:	https://github.com/ossc-db/%{sname}/archive/VERSION%{pgbulkloadpackagever}.tar.gz
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel pam-devel
BuildRequires:	libsepol-devel readline-devel krb5-devel
Requires:	postgresql%{pgmajorversion}-server %{sname}_%{pgmajorversion}-client

Obsoletes:	%{sname} <= %{version}-1
Obsoletes:	%{sname}%{pgmajorversion} < 3.1.16-2

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%package client
Summary:	High speed data loading utility for PostgreSQL
Requires:	postgresql%{pgmajorversion}-libs

%description client
pg_bulkload client subpackage provides client-only tools.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_bulkload
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pg_bulkload
%endif

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

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

%files client
%defattr(-,root,root)
%{pginstdir}/bin/pg_bulkload
%{pginstdir}/bin/postgresql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.20-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Jan 16 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.20-1
- Update to 3.1.20

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Apr 27 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-2
- Split llvmjit into its own subpackage.

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-1
- Update to 3.1.19

* Thu Jun 24 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.18-2
- Unbreak pg_bulkload installation.

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.18-1
- Update to 3.1.18

* Thu Apr 15 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.17-1
- Update to 3.1.17
- Export PATH, and remove pgxs patches.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.16-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

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
