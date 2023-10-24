%global sname pg_cron

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Run periodic jobs in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.6.2
Release:	1PGDG%{dist}
License:	AGPLv3
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	libopenssl1_0_0
%else
%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.0.2k
%endif
%endif

%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif

%description
pg_cron is a simple cron-based job scheduler for PostgreSQL
(9.5 or higher) that runs inside the database as an extension.
It uses the same syntax as regular cron, but it allows you to
schedule PostgreSQL commands directly from the database.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_cron
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
This packages provides JIT support for pg_cron
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1PGDG
- Update to 1.6.2, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.2

* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1PGDG
- Update to 1.6.1, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.1

* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1PGDG
- Update to 1.6.0, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 10 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.2

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.0
  and
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Aug 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2
- Add a (temp) patch to fix builds on Fedora 36, per
  https://github.com/citusdata/pg_cron/issues/187

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-2
- Fix SLES dependencies, per report from Tiago ANASTACIO.

* Mon Sep 27 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2
- Remove pgxs patches, and export PATH instead.

* Thu Apr 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Thu Oct 8 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.4-1
- Update to 1.1.4

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.3-2
- Rebuild against PostgreSQL 11.2

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository,
