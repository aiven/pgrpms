%global sname	hypopg

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Hypothetical Indexes support for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/HypoPG/hypopg/archive/%{version}.tar.gz
URL:		https://github.com/HypoPG/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
HypoPG is a PostgreSQL extension adding support for hypothetical indexes.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for hypopg
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
This packages provides JIT support for hypopg
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/import/*.bc
%endif

%changelog
* Tue Aug 1 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-2PGDG
- Cleanup rpmlint warnings
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon May 29 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Wed Jan 11 2023 John Harvey <john.harvey@crunchydata.com> - 1.3.1-3
- Update license type

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 23 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Tue Mar 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Thu Jul 9 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-1
- Update to 1.1.4

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-2
- Switch to using pgdg-srpm-macros dependency

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1
- Update to 1.1.3

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1
- Update to 1.1.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Mar 29 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1
- Update URLs

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
