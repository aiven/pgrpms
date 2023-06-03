%global debug_package %{nil}
%global sname pg_auto_failover

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Postgres extension and service for automated failover and high-availability
Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	2%{dist}.1
License:	Apache
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{sname}/
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

%description
pg_auto_failover is an extension and service for PostgreSQL that monitors and
manages automated failover for a Postgres cluster. It is optimized for
simplicity and correctness and supports Postgres 10 and newer.

We set up one PostgreSQL server as a monitor node as well as a primary and
secondary node for storing data. The monitor node tracks the health of the
data nodes and implements a failover state machine. On the PostgreSQL nodes,
the pg_autoctl program runs alongside PostgreSQL and runs the necessary
commands to configure synchronous streaming replication.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_auto_failover
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
This packages provides JIT support for pg_auto_failover
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md docs/
%{pginstdir}/bin/pg_autoctl
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/pgautofailover.so
%{pginstdir}/share/extension/pgautofailover-*.sql
%{pginstdir}/share/extension/pgautofailover.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/pgautofailover*.bc
    %{pginstdir}/lib/bitcode/pgautofailover/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 7 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-2
- Update SLES 15 dependencies for SP4.

* Thu Apr 7 2022 Devrim Gündüz <devrim@gunduz.org> 1.6.4-1
- Update to 1.6.4

* Wed Nov 10 2021 Devrim Gündüz <devrim@gunduz.org> 1.6.3-1
- Update to 1.6.3

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> 1.6.2-2
- Rebuild against LLVM 11 on SLES 15.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Wed Sep 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1
- Update to 1.6.2

* Thu Jul 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-2
- Add llvmjit subpackage (and also fix RHEL 8 - ppc64le builds)

* Thu Jul 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2

* Thu Apr 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Sun Dec 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1
- Require -contrib subpackage, per:
  https://github.com/citusdata/pg_auto_failover/issues/558

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Sun Jun 14 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0
- Depend on new pgdg-srpm-macros RPM.

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1
- Update to 1.0.5

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3
- Fix OS versions in Makefile, the distro name in the packages changed.

* Mon Jun 3 2019 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
