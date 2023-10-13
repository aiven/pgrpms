%global sname orafce
%global orafcemajver 4
%global orafcemidver 7
%global orafceminver 0

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{orafcemajver}.%{orafcemidver}.%{orafceminver}
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}.tar.gz
URL:		https://github.com/%{sname}/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel
BuildRequires:	pgdg-srpm-macros krb5-devel, bison, flex
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 3.13.4-2

%description
The goal of this project is implementation some functions from Oracle database.
Some date functions (next_day, last_day, trunc, round, ...) are implemented
now. Functionality was verified on Oracle 10g and module is useful
for production work.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for XXX
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
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for XXX
%endif

%prep
%setup -q -n %{sname}-VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/COPYRIGHT.%{sname}
%doc %{pginstdir}/doc/extension/INSTALL.%{sname}
%doc %{pginstdir}/doc/extension/README.asciidoc
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Oct 13 2023 Devrim Gündüz <devrim@gunduz.org> 4.7.0-1PGDG
- Update to 4.7.0

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> 4.6.1-1PGDG
- Update to 4.6.1

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> 4.6.0-1PGDG
- Update to 4.6.0

* Mon Aug 7 2023 Devrim Gündüz <devrim@gunduz.org> 4.5.0-1PGDG
- Update to 4.5.0

* Wed Jul 5 2023 Devrim Gündüz <devrim@gunduz.org> 4.4.0-1PGDG
- Update to 4.4.0
- Add PGDG branding

* Sun Jun 4 2023 Devrim Gündüz <devrim@gunduz.org> 4.3.0-1
- Update to 4.3.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.6-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 2 2023 Devrim Gündüz <devrim@gunduz.org> 4.2.6-1
- Update to 4.2.6

* Mon Apr 3 2023 Devrim Gündüz <devrim@gunduz.org> 4.2.4-1
- Update to 4.2.4

* Mon Mar 13 2023 Devrim Gündüz <devrim@gunduz.org> 4.2.1-1
- Update to 4.2.1

* Sun Mar 12 2023 Devrim Gündüz <devrim@gunduz.org> 4.2.0-1
- Update to 4.2.0

* Mon Jan 30 2023 Devrim Gündüz <devrim@gunduz.org> 4.1.1-1
- Update to 4.1.1

* Thu Jan 5 2023 Devrim Gündüz <devrim@gunduz.org> 4.1.0-1
- Update to 4.1.0

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> 4.0.2-1
- Update to 4.0.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Nov 22 2022 Devrim Gündüz <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1

* Thu Nov 3 2022 Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0

* Tue Oct 25 2022 Devrim Gündüz <devrim@gunduz.org> 3.25.1-1
- Update to 3.25.1

* Thu Oct 6 2022 Devrim Gündüz <devrim@gunduz.org> 3.25.0-1
- Update to 3.25.0

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> 3.24.4-2
- Add llvm subpackage to fix RHEL 8 - ppc64le builds.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> 3.24.4-1
- Update to 3.24.4

* Mon Aug 1 2022 Devrim Gündüz <devrim@gunduz.org> 3.24.0-1
- Update to 3.24.0

* Mon Jul 25 2022 Devrim Gündüz <devrim@gunduz.org> 3.22.1-1
- Update to 3.22.1

* Mon Jul 18 2022 Devrim Gündüz <devrim@gunduz.org> 3.22.0-1
- Update to 3.22.0

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> 3.21.1-1
- Update to 3.21.1

* Sun Apr 17 2022 Devrim Gündüz <devrim@gunduz.org> 3.21.0-1
- Update to 3.21.0

* Thu Apr 7 2022 Devrim Gündüz <devrim@gunduz.org> 3.20.0-1
- Update to 3.20.0

* Tue Jan 18 2022 Devrim Gündüz <devrim@gunduz.org> 3.18.1-1
- Update to 3.18.1

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> 3.18.0-1
- Update to 3.18.0

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> 3.17.0-1
- Update to 3.17.0

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 3.16.2-1
- Update to 3.16.2

* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> 3.16.0-1
- Update to 3.16.0-1

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> 3.15.1-1
- Update to 3.15.1

* Mon Mar 15 2021 Devrim Gündüz <devrim@gunduz.org> 3.15.0-1
- Update to 3.15.0

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> - 3.14.0-2
- Export PATH for pg_config, to get rid of patches.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> 3.14.0-1
- Update to 3.14.0

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 3.13.4-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> 3.13.4-1
- Update to 3.13.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> 3.11.1-1
- Update to 3.11.1

* Tue Feb 25 2020 Devrim Gündüz <devrim@gunduz.org> 3.9.0-1
- Update to 3.9.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Fri May 24 2019 Devrim Gündüz <devrim@gunduz.org> 3.8.0-1
- Update to 3.8.0

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> 3.7.2-1
- Update to 3.7.2

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Sat Feb 17 2018 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1
- Update to 3.6.1, per #3131
- Remove patch1, not needed anymore.

* Thu Oct 19 2017 - Devrim Gündüz <devrim@gunduz.org> 3.6.0-1
- Update to 3.6.0, per #2812

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 3.4.0-1
- Update to 3.4.0, per #2343.
- Add support for Power RPMs.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1

* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Fri Feb 19 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 3.1.2-1
- Update to 3.1.2

* Tue Jan 20 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.14-1
- Update to 3.0.14

* Wed Oct 22 2014 - Devrim Gündüz <devrim@gunduz.org> 3.0.7-1
- Update to 3.0.7

* Thu Sep 13 2012 - Devrim Gündüz <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Fri Oct 2 2009 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Remove patch0, it is in upstream now.
- Apply some 3.0 fixes to spec.

* Wed Aug 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.3-2
- Spec file fixes, per bz review #251805

* Mon Jan 14 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Fri Aug 10 2007 - Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial packaging
