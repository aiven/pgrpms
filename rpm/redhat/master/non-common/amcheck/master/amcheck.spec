%global sname amcheck

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Functions for verifying PostgreSQL relation integrity
Name:		%{sname}_next_%{pgmajorversion}
Version:	1.5
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/petergeoghegan/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/petergeoghegan/amcheck
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}_next%{pgmajorversion} <= 1.5-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
The amcheck module provides functions that allow you to verify the
logical consistency of the structure of PostgreSQL indexes. If the
structure appears to be valid, no error is raised. Currently, only
B-Tree indexes are supported, although since in practice the
majority of PostgreSQL indexes are B-Tree indexes, amcheck is
likely to be effective as a general corruption smoke-test in
production PostgreSQL installations.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
# Rename README file:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}_next.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}_next.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.md
%else
%license LICENSE.md
%endif
%{pginstdir}/lib/%{sname}_next.so
%{pginstdir}/share/extension/%{sname}_next*.sql
%{pginstdir}/share/extension/%{sname}_next.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}_next*.bc
   %{pginstdir}/lib/bitcode/%{sname}_next/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.5-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Feb 8 2019 Devrim Gündüz <devrim@gunduz.org> 1.5-1
- Update to 1.5

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Aug 20 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-4
- Fix .bc file path

* Sat Aug 11 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-3
- Ignore .bc files on PPC arch.

* Thu Aug 2 2018 - John Harvey <john.harvey@crunchydata.com> 1.4-2
- Support for PG11

* Thu Apr 26 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4, per #3314

* Tue Dec 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3, per #2972

* Thu Oct 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2, to fix RHEL 6 build issues, per #2814.

* Sat Oct 21 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1, per #2814.

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Update to 1.0

* Mon Oct 9 2017 - Devrim Gündüz <devrim@gunduz.org> 0.3-1
- Initial packaging for PostgreSQL RPM repository.

