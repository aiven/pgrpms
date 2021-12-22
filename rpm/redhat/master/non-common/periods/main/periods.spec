%global	sname	periods

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PERIODs and SYSTEM VERSIONING for PostgreSQL

Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	2%{?dist}
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	https://github.com/xocolatl/%{sname}/archive/v%{version}.zip
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This extension recreates the behavior defined in SQL:2016 (originally in
SQL:2011) around periods and tables with SYSTEM VERSIONING. The idea is to
figure out all the rules that PostgreSQL would like to adopt (there are some
details missing in the standard) and to allow earlier versions of PostgreSQL
to simulate the behavior once the feature is finally integrated.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%doc %{pginstdir}/doc/extension/README.periods
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
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
* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2-2
- Remove PGXS patches, and export PATH instead.

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Add a patch to fix RHEL 7 builds, per Vik.

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Fix OS versions in Makefile, the distro name in the packages changed.

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
