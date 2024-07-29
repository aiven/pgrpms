%global sname	pg_background

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Background Worker
Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/vibhorkum/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vibhorkum/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
This module allows user to arbitrary command in a background worker and
gives capability to users to launch

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_background
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
This packages provides JIT support for pg_background
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Sun Apr 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu May 20 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
