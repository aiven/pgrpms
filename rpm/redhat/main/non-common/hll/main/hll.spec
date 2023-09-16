%global sname hll

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension adding HyperLogLog data structures as a native data type
Name:		%{sname}_%{pgmajorversion}
Version:	2.18
Release:	1PGDG%{dist}
License:	Apache
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
This Postgres module introduces a new data type hll which is a
HyperLogLog data structure. HyperLogLog is a fixed-size, set-like
structure used for distinct value counting with tunable precision. For
example, in 1280 bytes hll can estimate the count of tens of billions of
distinct values with only a few percent error.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for hll
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
This packages provides JIT support for hll
%endif

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
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
* Sat Sep 16 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.18-1PGDG
- Update to 2.18
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.17-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.17-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Sep 21 2022 - Devrim Gündüz <devrim@gunduz.org> - 2.17-1
- Update to 2.17

* Mon Sep 13 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.16-1
- Update to 2.16

* Wed Dec 16 2020 - Devrim Gündüz <devrim@gunduz.org> - 2.15.1-1
- Update to 2.15.1

* Mon Nov 30 2020 - Devrim Gündüz <devrim@gunduz.org> 2.15-1
- Update to 2.15

* Sun Jun 14 2020 - Devrim Gündüz <devrim@gunduz.org> 2.14-1
- Update to 2.14

* Wed Nov 6 2019 - Devrim Gündüz <devrim@gunduz.org> 2.13-1
- Update to 2.13

* Tue Apr 16 2019 - Devrim Gündüz <devrim@gunduz.org> 2.12-1
- Update to 2.12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Sun Aug 26 2018 - Devrim Gündüz <devrim@gunduz.org> 2.11-1
- Update to 2.11
- Install PostgreSQL 11+ bitcode files

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.10.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
