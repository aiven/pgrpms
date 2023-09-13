%global debug_package %{nil}
%global sname	pg_ivm

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Incremental View Maintenance (IVM) feature for PostgreSQL.
Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}/
Source0:	https://github.com/sraoss/%{sname}/archive/refs/tags/v%{version}.tar.gz

%description
Incremental View Maintenance (IVM) is a way to make materialized views
up-to-date in which only incremental changes are computed and applied on
views rather than recomputing the contents from scratch as REFRESH
MATERIALIZED VIEW does. IVM can update materialized views more efficiently
than recomputation when only small parts of the view are changed.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_ivm
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
This packages provides JIT support for pg_ivm
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7

* Mon Sep 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6-1PGDG
- Update to 1.6
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Mar 2 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Tue Feb 7 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5

* Tue Dec 20 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Update to 1.0

* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-alpha-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
