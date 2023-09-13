%global sname pg_stat_monitor

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Query Performance Monitoring Tool
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.2
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/percona/%{sname}
Source0:	https://github.com/percona/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.1.3-2

%description
The pg_stat_monitor is a PostgreSQL Query Performance Monitoring tool, based
on PostgreSQL's contrib module pg_stat_statements. PostgreSQL’s
pg_stat_statements provides the basic statistics, which is sometimes not
enough. The major shortcoming in pg_stat_statements is that it accumulates
all the queries and their statistics and does not provide aggregated
statistics nor histogram information. In this case, a user needs to calculate
the aggregate which is quite expensive.

pg_stat_monitor is developed on the basis of pg_stat_statements as its more
advanced replacement. It provides all the features of pg_stat_statements
plus its own feature set.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_monitor
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
This packages provides JIT support for pg_stat_monitor
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Sep 13 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1PGDG
- Update to 2.0.2
- Cleanup rpmlint warning

* Tue Jun 20 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1PGDG
- Update to 2.0.1
- Add PGDG suffix to the package.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Sep 19 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue May 31 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Fri May 6 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Tue Jan 4 2022 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-rc.1
- Update to 1.0.0-rc.1

* Fri Sep 24 2021 - Devrim Gündüz <devrim@gunduz.org> 0.9.2-beta1
- Update to 0.9.2 beta1

* Thu Apr 15 2021 - Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1

* Thu Jan 28 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-2
- Fix distro part in RPM names.

* Thu Jan 21 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
