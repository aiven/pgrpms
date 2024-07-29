%global sname pg_similarity
%global packagemajorver 1
%global packageminver 0

%{!?llvm:%global llvm 1}

Summary:	Set of functions and operators for executing similarity queries for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{packagemajorver}.%{packageminver}
Release:	2PGDG%{?dist}
URL:		https://github.com/eulerto/%{sname}
Source0:	https://github.com/eulerto/%{sname}/archive/refs/tags/%{sname}_%{packagemajorver}_%{packageminver}.tar.gz
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_similarity module provides full text search capability in PostgreSQL.
This module allows a user to create 2-gram (bigram) index for faster
full text search.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_similarity
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pg_similarity
%endif

%prep
%setup -q -n %{sname}-%{sname}_%{packagemajorver}_%{packageminver}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Apr 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

