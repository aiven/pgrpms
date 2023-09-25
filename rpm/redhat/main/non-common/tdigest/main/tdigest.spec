%global sname tdigest

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	t-digest implementation for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/tvondra/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/tvondra/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements t-digest, a data structure for on-line
accumulation of rank-based statistics such as quantiles and trimmed means.
The algorithm is also very friendly to parallel programs.

The accuracy of estimates produced by t-digests can be orders of magnitude
more accurate than those produced by previous digest algorithms in spite of
the fact that t-digests are much more compact when stored on disk.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for tdigest
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
This packages provides JIT support for tdigest
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif


%changelog
* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> 1.4.1-1PGDG
- Update to 1.4.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Apr 17 2022 Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.0.1-2
- Remove pgxs patches, and export PATH instead.

* Thu Nov 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
