%global pgbigmpackagever 20240606
%global pgbigmver 1.2
%global sname pg_bigm

%{!?llvm:%global llvm 1}

Summary:	2-gram (bigram) index for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgbigmver}_%{pgbigmpackagever}
Release:	1PGDG%{?dist}
URL:		https://github.com/pgbigm/%{sname}
Source0:	https://github.com/pgbigm/%{sname}/archive/refs/tags/v%{pgbigmver}-%{pgbigmpackagever}.tar.gz
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

%description llvmjit
This packages provides JIT support for pg_bigm
%endif

%prep
%setup -q -n %{sname}-%{pgbigmver}-%{pgbigmpackagever}

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
* Wed Jun 26 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20240606-1PGDG
- Update to 1.2-20240606 per changes described at:
  https://github.com/pgbigm/pg_bigm/releases/tag/v1.2-20240606

* Wed Apr 3 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20200228-1PGDG
- Initial packaging for the PostgreSQL RPM repository

