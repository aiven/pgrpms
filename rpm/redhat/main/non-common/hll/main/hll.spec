%global sname hll

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL extension adding HyperLogLog data structures as a native data type
Name:		%{sname}_%{pgmajorversion}
Version:	2.17
Release:	1%{dist}
License:	Apache
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This Postgres module introduces a new data type hll which is a
HyperLogLog data structure. HyperLogLog is a fixed-size, set-like
structure used for distinct value counting with tunable precision. For
example, in 1280 bytes hll can estimate the count of tens of billions of
distinct values with only a few percent error.

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
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
* Wed Sep 21 2022 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.17

* Mon Sep 13 2021 - Devrim Gündüz <devrim@gunduz.org> 2.16-1
- Update to 2.16

* Wed Dec 16 2020 - Devrim Gündüz <devrim@gunduz.org> 2.15.1-1
- Update to 2.15.1

* Mon Nov 30 2020 - Devrim Gündüz <devrim@gunduz.org> 2.15-1
- Update to 2.15

* Sun Jun 14 2020 - Devrim Gündüz <devrim@gunduz.org> 2.14-1
- Update to 2.14

* Wed Nov 6 2019 - Devrim Gündüz <devrim@gunduz.org> 2.13-1
- Update to 2.13

* Tue Apr 16 2019 - Devrim Gündüz <devrim@gunduz.org> 2.12-1
- Update to 2.12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Sun Aug 26 2018 - Devrim Gündüz <devrim@gunduz.org> 2.11-1
- Update to 2.11
- Install PostgreSQL 11+ bitcode files

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.10.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
