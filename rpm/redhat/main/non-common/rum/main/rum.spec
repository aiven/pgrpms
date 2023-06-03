%global sname	rum

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	RUM access method - inverted index with additional information in posting lists
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.13
Release:	2%{?dist}.1
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
The rum module provides access method to work with RUM index.
It is based on the GIN access methods code.

%package devel
Summary:	RUM access method development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package includes the development headers for the rum extension.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for rum
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
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for rum
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/include/server
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install}  -d %{buildroot}%{pginstdir}/doc/extension
%{__install}  -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
  %{pginstdir}/lib/bitcode/%{sname}*.bc
  %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/rum*.h

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3.13-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.13-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 10 2022 Devrim Gündüz <devrim@gunduz.org> 1.3.13-1
- Update to 1.3.13
- Split llvm into its own subpackage.

* Tue Jun 14 2022 Devrim Gündüz <devrim@gunduz.org> 1.3.11-1
- Update to 1.3.11

* Fri Jun 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.3.8-1
- Update to 1.3.8

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.3.7-2
- Remove pgxs patches, and  export PATH instead.

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> 1.3.7-1
- Update to 1.3.7

* Wed Apr 1 2020 Devrim Gündüz <devrim@gunduz.org> 1.3.1-2
- Add missing BR and Requires
- Switch to pgdg-srpm-macros
- Fix rpmlint warning

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 1.2.1-2
- Rebuild against PostgreSQL 11.0

* Tue Jul 3 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
