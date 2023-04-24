%global sname postgresql-unit

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	SI Units for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	7.7
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/ChristophBerg/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
postgresql-unit implements a PostgreSQL datatype for SI units, plus byte.
The base units can be combined to named and unnamed derived units using
operators defined in the PostgreSQL type system. SI prefixes are used for
input and output, and quantities can be converted to arbitrary scale.

Requires PostgreSQL 9.5 or later (uses psprintf()), flex, and bison 3 (the
pre-built grammar files are used if only bison 2 is available).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql-unit
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for postgresql-unit
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH  %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/unit.so
%{pginstdir}/share/extension/unit*.sql
%{pginstdir}/share/extension/unit.control
%{pginstdir}/share/extension/unit_prefixes.data
%{pginstdir}/share/extension/unit_units.data

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/uni*.bc
   %{pginstdir}/lib/bitcode/unit/*.bc
%endif

%changelog
* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 7.7-1
- Update to 7.7

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org>- 7.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 7.4-1
- Update to 7.4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 7.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>- 7.2-1.1
- Rebuild for PostgreSQL 12

* Thu Sep 5 2019 Devrim Gündüz <devrim@gunduz.org> 7.2-1
- Update to 7.2

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> 7.1-1
- Update to 7.1

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> 7.0-1
- Update to 7.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 6.0-2.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-2
- Add v11+ bitcode conditionals

* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Sun May 28 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Thu Apr 27 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0
- Add support for Power RPMs.

* Tue Jan 10 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Sep 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
