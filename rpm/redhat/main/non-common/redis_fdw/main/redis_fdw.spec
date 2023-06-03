%global sname	redis_fdw

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	A PostgreSQL Foreign Data Wrapper for Redis
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	3%{?dist}.2
License:	PostgreSQL
URL:		https://github.com/nahanni/rw_redis_fdw/
Source0:	https://github.com/nahanni/rw_redis_fdw/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel hiredis-devel
BuildRequires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-server hiredis

%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	glibc-devel
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires:	libnsl
%endif

# Packages come from EPEL and SCL:
%if 0%{?rhel} && 0%{?rhel} == 7
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
Requres:	llvm15
%endif

%description
Writable Foreign Data Wrapper for Redis

This PostgreSQL extension provides a Foreign Data Wrapper for read (SELECT)
and write (INSERT, UPDATE, DELETE) access to Redis databases
(http://redis.io). Supported Redis data types include: string, set, hash,
list, zset, and pubsub.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for redis_fdw
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
This packages provides JIT support for redis_fdw
%endif

%prep
%setup -q -n rw_redis_fdw-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if %runselftest
PATH=%{pginstdir}/bin/:$PATH %{__make} installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres PGPORT=5495
%endif

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-3.2
- Rebuild against LLVM 15 on SLES 15

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org>- 1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Remove pxgs patches, and export PATH instead.

* Mon Aug 17 2020 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1, which supports PostgreSQL 13.

* Wed May 6 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Fix suffixes in RPMs.

* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM for the PostgreSQL RPM repository
