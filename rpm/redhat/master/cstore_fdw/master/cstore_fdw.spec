%global sname cstore_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Columnar store extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.7.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://citusdata.github.io/cstore_fdw/
%if 0%{?suse_version} >= 1315
BuildRequires:	protobuf-c libprotobuf-c-devel
%else
BuildRequires:	protobuf-c-devel
%endif
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
cstore_fdw is column-oriented store available for PostgreSQL. Using it will
let you:
    Leverage typical analytics benefits of columnar stores
    Deploy on stock PostgreSQL or scale-out PostgreSQL (CitusDB)

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-cstore_fdw.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Feb 18 2020 - Devrim Gündüz <devrim@gunduz.org> 1.7.0-1
- Update to 1.7.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Tue Sep 4 2018 - Devrim Gündüz <devrim@gunduz.org> 1.6.2-1
- Update to 1.6.2
- Add .bc bits to spec file

* Sun Jun 3 2018 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1, per #3395

* Sun Jul 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0
- Add LICENSE among installed files.

* Thu Jun 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4
- Parallel build seems to be broken, so disable it for now.

* Mon Sep 07 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Aug 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
