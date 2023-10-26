%global sname	passwordcheck_cracklib

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	3.0.0
Release:	2PGDG%{?dist}
Summary:	PostgreSQL passwordcheck extension, built with cracklib.
License:	BSD
URL:		https://github.com/devrimgunduz/%{sname}/
Source0:	https://github.com/devrimgunduz/%{sname}/archive/%{version}.tar.gz
Requires:	postgresql%{pgmajorversion} cracklib cracklib-dicts

BuildRequires:	cracklib-devel postgresql%{pgmajorversion}-devel pgdg-srpm-macros

%description
This is the regular PostgreSQL passwordcheck extension, built with cracklib.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for passwordcheck_cracklib
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
This packages provides JIT support for passwordcheck_cracklib
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-2PGDG
- Add PGDG branding
- Clean up rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Jan 12 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jan 27 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Remove PGXS patches, and use PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.2-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Add v11 code to spec file

* Tue May 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial packaging
