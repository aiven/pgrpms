%global sname pg_cron

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Run periodic jobs in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.2
Release:	1%{dist}
License:	AGPLv3
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-1.4.2-makefile.patch
URL:		https://github.com/citusdata/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	openssl
%else
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	libopenssl1_0_0
%else
%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.0.2k
%endif
%endif
%endif

# We depend un the SSL libraries provided by Advance Toolchain on PPC,
# so use openssl-devel only on other platforms:
%ifnarch ppc64 ppc64le
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pg_cron is a simple cron-based job scheduler for PostgreSQL
(9.5 or higher) that runs inside the database as an extension.
It uses the same syntax as regular cron, but it allows you to
schedule PostgreSQL commands directly from the database.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
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
