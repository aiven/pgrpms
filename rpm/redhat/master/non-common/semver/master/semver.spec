%global sname semver

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	A semantic version data type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.31.1
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/theory/pg-%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/theory/pg-semver/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.31.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This library contains a single PostgreSQL extension, a data type called "semver".
It's an implementation of the version number format specified by the Semantic
Versioning 2.0.0 Specification.

%prep
%setup -q -n pg-%{sname}-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/semver.mmd
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/src/%{sname}*.bc
   %{pginstdir}/lib/bitcode/src/%{sname}/src/*.bc
  %endif
 %endif
%endif


%changelog
* Tue Apr 27 2021 Devrim Gündüz <devrim@gunduz.org> - 0.31.1-1
- Update to 0.31.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.31.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Oct 19 2020 Devrim Gündüz <devrim@gunduz.org> - 0.31.0-1
- Update to 0.31.0

* Mon Jun 1 2020 Devrim Gündüz <devrim@gunduz.org> - 0.30.0-1
- Update to 0.30.0

* Sat Apr 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.22.0-1
- Update to 0.22.0

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> - 0.21.0-1
- Initial packaging for PostgreSQL RPM Repository
