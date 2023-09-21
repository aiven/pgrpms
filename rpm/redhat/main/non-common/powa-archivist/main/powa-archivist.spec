%global __python %{_bindir}/python3
%global sname powa

# Powa archivist version
%global powamajorversion 4
%global powamidversion 2
%global powaminorversion 0

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Workload Analyzer Archivist
Name:		%{sname}-archivist_%{pgmajorversion}
Version:	%{powamajorversion}.%{powamidversion}.%{powaminorversion}
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/powa-team/powa-archivist/archive/REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}.tar.gz
URL:		https://powa.readthedocs.io/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.

It is similar to Oracle AWR or SQL Server MDW.

This is the core extension of the PoWA project, a PostgreSQL Workload Analyzer
that gathers performance stats and provides real-time charts and graphs to help
monitor and tune your PostgreSQL servers.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for powa
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
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
This packages provides JIT support for powa
%endif

%prep
%setup -q -n %{sname}-archivist-REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Move powa docs into their own subdirectory:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/%{sname}
%{__install} INSTALL.md LICENSE.md PL_funcs.md README.md %{buildroot}%{pginstdir}/doc/extension/%{sname}

%files
%defattr(-,root,root,-)
%dir %{pginstdir}/doc/extension/%{sname}
%doc %{pginstdir}/doc/extension/%{sname}/INSTALL.md
%doc %{pginstdir}/doc/extension/%{sname}/PL_funcs.md
%doc %{pginstdir}/doc/extension/%{sname}/README.md
%license %{pginstdir}/doc/extension/%{sname}/LICENSE.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

