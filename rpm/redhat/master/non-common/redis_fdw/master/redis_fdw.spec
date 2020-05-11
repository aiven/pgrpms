%global sname	redis_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

Summary:	A PostgreSQL Foreign Data Wrapper for Redis
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2%{?dist}
License:	PostgreSQL
URL:		https://github.com/nahanni/rw_redis_fdw/
Source0:	https://github.com/nahanni/rw_redis_fdw/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel hiredis-devel
BuildRequires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-server hiredis

%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	glibc-devel
# Packages come from EPEL and SCL:
BuildRequires:	llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 5.0.1
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires:	libnsl
BuildRequires:	llvm-devel >= 6.0.0 clang-devel >= 6.0.0
%endif
%if 0%{?fedora}
BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif


%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
Writable Foreign Data Wrapper for Redis

This PostgreSQL extension provides a Foreign Data Wrapper for read (SELECT)
and write (INSERT, UPDATE, DELETE) access to Redis databases
(http://redis.io). Supported Redis data types include: string, set, hash,
list, zset, and pubsub.

%prep
%setup -q -n rw_redis_fdw-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
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
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Wed May 6 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Fix suffixes in RPMs.

* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM for the PostgreSQL RPM repository
