%global debug_package %{nil}
%global sname plpgsql_check

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.3
Release:	1%{?dist}
Summary:	Additional tools for PL/pgSQL functions validation

License:	BSD
URL:		https://github.com/okbob/%{sname}
Source0:	https://github.com/okbob/%{sname}/archive/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
The plpgsql_check is PostgreSQL extension with functionality for direct
or indirect extra validation of functions in PL/pgSQL language. It verifies
a validity of SQL identifiers used in PL/pgSQL code. It also tries to identify
performance issues.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plpgsql_check
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
This packages provides JIT support for plpgsql_check
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
 %ifarch ppc64 ppc64le
  %else
  %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
   %if 0%{?rhel} && 0%{?rhel} <= 6
   %else
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
   %endif
  %endif
 %endif
%endif

%changelog
* Thu Apr 7 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Tue Feb 1 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.5-2
- Rebuild against LLVM 11 on SLES 15.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Thu Sep 30 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Mon Jul 26 2021 Devrim Gündüz <devrim@gunduz.org> 1.17.1-1
- Update to 1.17.1

* Mon Jun 21 2021 Devrim Gündüz <devrim@gunduz.org> 1.17.0-1
- Update to 1.17.0

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.16.0-1
- Update to 1.16.0

* Thu Feb 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.3-2
- Split llvmjit into separate package

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.3-1
- Update to 1.15.3

* Fri Feb 5 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.2-1
- Update to 1.15.2

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.1-2
- export PATH for pg_config, to get rid of patches.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> 1.15.1-1
- Update to 1.15.1

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> 1.13.1-1
- Update to 1.13.1

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> 1.11.4-1
- Update to 1.11.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.2-1
- Update to 1.9.2

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0
- Switch to pgdg-srpm-macros

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.6-1
- Update to 1.7.6

* Thu Aug 15 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.4-1
- Update to 1.7.4

* Wed Jul 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.3-1
- Update to 1.7.3

* Fri Apr 26 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.1-1
- Update to 1.7.1

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 19 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Fri Sep 15 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1, per #2711

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.0.5

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Tue Jan 20 2015 - Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3

* Mon Aug 25 2014 - Pavel STEHULE <pavel.stehule@gmail.com> 0.9.2-1
- Initial packaging
