%global sname pgmeminfo

%global pmeminfomajver 1
%global pmeminfomidver 0
%global pmeminfominver 0

Name:		%{sname}_%{pgmajorversion}
Version:	%{pmeminfomajver}.%{pmeminfomidver}.%{pmeminfominver}
Release:	1PGDG%{?dist}
Summary:	PostgreSQL extension to allow to access to memory usage diagnostics
License:	BSD
URL:		https://github.com/okbob/%{sname}
Source0:	https://github.com/okbob/pgmeminfo/archive/refs/tags/VERSION_%{pmeminfomajver}_%{pmeminfomidver}_%{pmeminfominver}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
The pgmeminfo extension can be used to display memory usage information of
a PostgreSQL server.

%package llvmjit
Summary:	Just-in-time compilation support for pgmeminfo
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pgmeminfo

%prep
%setup -q -n %{sname}-VERSION_%{pmeminfomajver}_%{pmeminfomidver}_%{pmeminfominver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/src/*.bc

%changelog
* Tue Mar 5 2024 Devrim Gündüz <devrim@gunduz.org> 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
