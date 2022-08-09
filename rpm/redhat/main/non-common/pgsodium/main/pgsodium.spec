%global sname pgsodium

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension for high level cryptographic algorithms
Name:		%{sname}_%{pgmajorversion}
Version:	3.0.2
Release:	1%{dist}
License:	BSD
URL:		https://github.com/michelp/%{sname}/
Source0:	https://github.com/michelp/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel libsodium-devel
Requires:	postgresql%{pgmajorversion}-server libsodium

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgsodium is an encryption library extension for PostgreSQL using the
libsodium library for high level cryptographic algorithms.

pgsodium can be used a straight interface to libsodium, but it can also use
a powerful feature called Server Key Management where pgsodium loads an
external secret key into memory that is never accessible to SQL. This
inaccessible root key can then be used to derive sub-keys and keypairs by
key id. This id (type bigint) can then be stored instead of the derived key.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsodium
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
BuildRequires:	llvm11-devel clang11-devel
%endif

%description llvmjit
This packages provides JIT support for pgsodium
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Tue Aug 9 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0

* Tue Feb 15 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
