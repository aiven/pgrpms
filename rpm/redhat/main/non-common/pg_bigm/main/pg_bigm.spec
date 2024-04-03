%global pgbigmpackagever 20200228
%global sname pg_bigm

%{!?llvm:%global llvm 1}

Summary:	2-gram (bigram) index for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	1PGDG%{?dist}
URL:		https://github.com/pgbigm/%{sname}
Source0:	https://github.com/pgbigm/%{sname}/releases/download/v%{version}-%{pgbigmpackagever}/%{sname}-%{version}-%{pgbigmpackagever}.tar.gz
# Upstream patch to fix v16 builds:
# https://github.com/pgbigm/pg_bigm/commit/34fe30fcb7dd58b6652e7cbf539f1615fcc0e47b
Patch0:		%{sname}-pg16-fixbuild.patch
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_bigm module provides full text search capability in PostgreSQL.
This module allows a user to create 2-gram (bigram) index for faster
full text search.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_bigm
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif

%description llvmjit
This packages provides JIT support for pg_bigm
%endif

%prep
%setup -q -n %{sname}-%{version}-%{pgbigmpackagever}
%patch -P 0 -p0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/pg_bigm.so
%{pginstdir}/share/extension/pg_bigm*.sql
%{pginstdir}/share/extension/pg_bigm.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Apr 3 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20200228-1PGDG
- Initial packaging for the PostgreSQL RPM repository

