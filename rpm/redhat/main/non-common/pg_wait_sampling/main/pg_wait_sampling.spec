%global sname	pg_wait_sampling

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Sampling based statistics of wait events
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.5
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
PostgreSQL 9.6+ provides an information about current wait event of particular
process. However, in order to gather descriptive statistics of server
behavior user have to sample current wait event multiple times.

pg_wait_sampling is an extension for collecting sampling statistics of wait
events.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_wait_sampling
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
This packages provides JIT support for pg_wait_sampling
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
* Fri Oct 20 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.5-1PGDG
- Update to 1.1.5
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.4-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 30 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-1
- Update to 1.1.4

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1
- Update to 1.1.3
- export PATH for pg_config, to get rid of patches.
- Fix license

* Wed Nov 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1
- Update to 1.1.2

* Sat Apr 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Initial packaging for PostgreSQL RPM Repository
