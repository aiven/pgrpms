%if 0%{?rhel} && 0%{?rhel} == 7
%global	debug_package %{nil}
%endif

%global _build_id_links none
%global sname citus

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension that transforms Postgres into a distributed database
Name:		%{sname}_%{pgmajorversion}
Version:	12.1.0
Release:	2PGDG%{dist}
License:	AGPLv3
URL:		https://github.com/citusdata/%{sname}
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
BuildRequires:	libxslt-devel openssl-devel pam-devel readline-devel
BuildRequires:	libcurl-devel pgdg-srpm-macros libzstd-devel
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?suse_version} >= 1315
Requires:	libzstd1
%else
Requires:	libzstd
%endif

%description
Citus horizontally scales PostgreSQL across commodity servers
using sharding and replication. Its query engine parallelizes
incoming SQL queries across these servers to enable real-time
responses on large datasets.

Citus extends the underlying database rather than forking it,
which gives developers and enterprises the power and familiarity
of a traditional relational database. As an extension, Citus
supports new PostgreSQL releases, allowing users to benefit from
new features while maintaining compatibility with existing
PostgreSQL tools. Note that Citus supports many (but not all) SQL
commands.

%package devel
Summary:	Citus development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for Citus.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for Citus
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
# Packages come from EPEL and SCL:
%ifarch aarch64
BuildRequires:	llvm-toolset-7.0-llvm-devel >= 7.0.1 llvm-toolset-7.0-clang >= 7.0.1
%else
BuildRequires:	llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 4.0.1
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
# Packages come from Appstream:
BuildRequires:	llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?fedora}
BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif

%description llvmjit
This packages provides JIT support for Citus
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%configure PG_CONFIG=%{pginstdir}/bin/pg_config
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/%{sname}_columnar.so
%{pginstdir}/lib/%{sname}_pgoutput.so
%{pginstdir}/lib/%{sname}_wal2json.so
%dir %{pginstdir}/lib/%{sname}_decoders/
%{pginstdir}/lib/%{sname}_decoders/pgoutput.so
%{pginstdir}/lib/%{sname}_decoders/wal2json.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_columnar-*.sql
%{pginstdir}/share/extension/columnar-*.sql
%{pginstdir}/share/extension/%{sname}_columnar.control

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/citus_version.h
%{pginstdir}/include/server/distributed/*.h

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
    %{pginstdir}/lib/bitcode/%{sname}_columnar/*
    %{pginstdir}/lib/bitcode/%{sname}_pgoutput/*
    %{pginstdir}/lib/bitcode/%{sname}_wal2json/*
%endif

%changelog
* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 12.1.0-1PGDG
- Update to 12.1.0

* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 12.0.0-2PGDG
- Remove RHEL 6 bits
- Remove rpmlint warning

* Wed Jul 19 2023 Devrim Gunduz <devrim@gunduz.org> - 12.0.0-1PGDG
- Update to 12.0.0
- Add PGDG branding

* Wed Jun 14 2023 Devrim Gunduz <devrim@gunduz.org> - 11.3.0-2
- Use _build_id_links macro to get rid of rpm build warnings, per:
  https://redmine.postgresql.org/issues/7815#note-5
- Disable debuginfo packaging on RHEL 7, to fix
  "canonicalization unexpectedly shrank by one character" issue.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 11.3.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 2 2023 Devrim Gündüz <devrim@gunduz.org> 11.3.0-1
- Update to 11.3.0

* Wed Apr 26 2023 Devrim Gündüz <devrim@gunduz.org> 11.2.1-1
- Update to 11.2.1

* Sat Feb 4 2023 Devrim Gündüz <devrim@gunduz.org> 11.2.0-1
- Update to 11.2.0

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> 11.1.5-1
- Update to 11.1.5

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 11.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 24 2022 Devrim Gündüz <devrim@gunduz.org> 11.1.4-1
- Update to 11.1.4

* Mon Oct 17 2022 Devrim Gündüz <devrim@gunduz.org> 11.1.3-1
- Update to 11.1.3

* Mon Oct 03 2022 Devrim Gündüz <devrim@gunduz.org> 11.1.2-1
- Update to 11.1.2

* Mon Sep 19 2022 Devrim Gündüz <devrim@gunduz.org> 11.1.1-1
- Update to 11.1.1

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.6-2
- Update SLES 15 requirements for SP4.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.6-1
- Update to 11.0.6

* Mon Aug 1 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.5-1
- Update to 11.0.5

* Thu Jul 14 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.4-1
- Update to 11.0.4

* Fri Jul 8 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.3-1
- Update to 11.0.3

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.2-2
- Update Summary.

* Sun Jun 19 2022 Devrim Gündüz <devrim@gunduz.org> 11.0.2-1
- Update to 11.0.2

* Mon Mar 21 2022 Devrim Gündüz <devrim@gunduz.org> 10.2.5-1
- Update to 10.2.5

* Wed Feb 2 2022 Devrim Gündüz <devrim@gunduz.org> 10.2.4-1
- Update to 10.2.4

* Mon Nov 29 2021 Devrim Gündüz <devrim@gunduz.org> 10.2.3-1
- Update to 10.2.3

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> 10.2.2-2
- Rebuild against LLVM 11 on SLES 15.
- Fix libzstd dependency name on SLES.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 10.2.2-1
- Update to 10.2.2

* Mon Sep 27 2021 Devrim Gündüz <devrim@gunduz.org> 10.2.1-1
- Update to 10.2.1

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> 10.2.0-1
- Update to 10.2.0

* Thu Aug 19 2021 Devrim Gündüz <devrim@gunduz.org> 10.1.2-1
- Update to 10.1.2

* Thu Aug 12 2021 Devrim Gündüz <devrim@gunduz.org> 10.1.1-1
- Update to 10.1.1

* Tue Jul 20 2021 Devrim Gündüz <devrim@gunduz.org> 10.1.0-1
- Update to 10.1.0

* Sun Mar 21 2021 Devrim Gündüz <devrim@gunduz.org> 10.0.3-1
- Update to 10.0.3

* Fri Mar 5 2021 Devrim Gündüz <devrim@gunduz.org> 10.0.2-1
- Update to 10.0.2

* Mon Feb 22 2021 Devrim Gündüz <devrim@gunduz.org> 10.0.1-2
- Split llvmjit into its own subpackage.

* Mon Feb 22 2021 Devrim Gündüz <devrim@gunduz.org> 10.0.1-1
- Update to 10.0.1

* Mon Feb 22 2021 Devrim Gündüz <devrim@gunduz.org> 9.5.4-1
- Update to 9.5.4

* Thu Jan 28 2021 Devrim Gündüz <devrim@gunduz.org> 9.5.2-1
- Update to 9.5.2

* Thu Dec 3 2020 Devrim Gündüz <devrim@gunduz.org> 9.5.1-1
- Update to 9.5.1

* Thu Oct 22 2020 Devrim Gündüz <devrim@gunduz.org> 9.5.0-1
- Update to 9.5.0

* Thu Oct 22 2020 Devrim Gündüz <devrim@gunduz.org> 9.4.2-1
- Update to 9.4.2

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> 9.4.1-1
- Update to 9.4.1

* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> 9.4.0-1
- Update to 9.4.0

* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> 9.3.5-1
- Update to 9.3.5

* Fri Jul 24 2020 Devrim Gündüz <devrim@gunduz.org> 9.3.4-1
- Update to 9.3.4

* Thu Jul 9 2020 Devrim Gündüz <devrim@gunduz.org> 9.3.2-1
- Update to 9.3.2

* Sun May 10 2020 Devrim Gündüz <devrim@gunduz.org> 9.3.0-1
- Update to 9.3.0

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.4-1
- Update to 9.2.4

* Thu Mar 26 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.3-1
- Update to 9.2.3

* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.2-1
- Update to 9.2.2

* Mon Feb 17 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.1-1
- Update to 9.2.1

* Tue Feb 11 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.0-1
- Update to 9.2.0

* Wed Jan 1 2020 Devrim Gündüz <devrim@gunduz.org> 9.1.2-1
- Update to 9.1.2

* Mon Dec 9 2019 Devrim Gündüz <devrim@gunduz.org> 9.1.0-1
- Update to 9.1.0

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> 9.0.1-1
- Update to 9.0.1

* Wed Oct 16 2019 Devrim Gündüz <devrim@gunduz.org> 9.0.0-1
- Update to 9.0.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.2-1
- Update to 8.3.2

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.1-1
- Update to 8.3.1

* Fri Jul 12 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.0-1
- Update to 8.3.0

* Thu Jun 13 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.2-1
- Update to 8.2.2

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.1-1
- Update to 8.2.1

* Mon Apr 1 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.0-1
- Update to 8.2.0

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 8.1.1-2
- Rebuild against PostgreSQL 11.2

* Tue Jan 15 2019 Devrim Gündüz <devrim@gunduz.org> 8.1.1-1
- Update to 8.1.1

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> 8.0.1-1
- Update to 8.0.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Aug 30 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.5.1-1
- Update to 7.5.1, per #3597

* Thu Jul 26 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.5.0-1
- Update to 7.5.0

* Fri Jun 29 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.4.1-1
- Update to 7.4.1, per #3432

* Thu May 17 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.4.0-1
- Update to 7.4.0, per #3351

* Fri Mar 16 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.3.0-1
- Update to 7.3.0, per #3208

* Tue Feb 6 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.2.1-1
- Update to 7.2.1, per #3088

* Thu Jan 18 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.2.0-1
- Update to 7.2.0, per #3026

* Wed Jan 10 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.1.2-1
- Update to 7.1.2, per #2994

* Sun Dec 10 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.1.1-1
- Update to 7.1.1, per #2938

* Thu Nov 16 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.1.0-1
- Update to 7.1.0

* Sat Oct 21 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.3-1
- Update to 7.0.3, per #2817

* Tue Oct 3 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.2-1
- Update to 7.0.2, per #2751

* Wed Sep 13 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.1-1
- Update to 7.0.1, per #2697.

* Thu Aug 31 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.0-1
- Update to 7.0.0

* Sat Jul 15 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.3-1
- Update to 6.2.3

* Sun Jun 11 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.2-1
- Update to 6.2.2

* Thu May 25 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.1-1
- Update to 6.2.1

* Tue Apr 25 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.1.0-1
- Update to 6.1.0

* Thu Dec 1 2016 - Devrim Gündüz <devrim@gunduz.org> 6.0.1-1
- Update to 6.0.1

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 6.0.0-1
- Update to 6.0.0
- Split development headers into separate subpackage.

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.2-1
- Update to 5.2.2

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0. Fixes #1566.
- Update license and install docs. Fixes #1385.

* Thu Jul 7 2016 - Devrim Gündüz <devrim@gunduz.org> 5.1.1-1
- Update to 5.1.1

* Tue May 17 2016 - Jason Petersen <jason@citusdata.com> 5.1.0-1
- Update to Citus 5.1.0

* Fri Mar 25 2016 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository,
  based on the spec file of Jason Petersen @ Citus.
