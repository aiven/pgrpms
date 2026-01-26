%global sname nominatim_fdw

%{!?llvm:%global llvm 1}

Summary:	Nominatim Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PGDG%{dist}
Source0:	https://github.com/jimjonesbr/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/jimjonesbr/%{sname}
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for nominatim_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for nominatim_fdw
%endif

%description
The nominatim_fdw is a PostgreSQL Foreign Data Wrapper to access data from
Nominatim servers using simple function calls.

%prep
%setup -q -n %{sname}-%{version}

%build
export PATH=%{pginstdir}/bin:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-, root, root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jan 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
