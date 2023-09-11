%global sname pgmp

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Multiple Precision Arithmetic Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	1PGDG%{?dist}
License:	LGPL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
# Make sure that we use Python 3.
Patch1:		%{sname}-python3.patch
URL:		https://dvarrazzo.github.io/pgmp/
BuildRequires:	postgresql%{pgmajorversion}-devel gmp-devel pgdg-srpm-macros
Requires:	gmp

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.4-3

%description
The pgmp extension adds PostgreSQL data types wrapping the high performance
integer and rational data types offered by the GMP library.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgmp
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
This packages provides JIT support for pgmp
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 1 -p0

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%doc README.rst
%license COPYING
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}*.sql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.5-1PGDG
- Update to 1.0.5
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-5.2
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-5.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-5
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Make sure that we use Python 3.

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jan 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
