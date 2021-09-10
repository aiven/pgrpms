%global debug_package %{nil}

%global sname	pg_repack

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Reorganize tables in PostgreSQL databases without any locks
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.6
Release:	3%{?dist}
License:	BSD
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://pgxn.org/dist/pg_repack/
Patch0:		277.patch

BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 1.4.6-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pg_repack can re-organize tables on a postgres database without any locks so that
you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH  %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root)
%doc COPYRIGHT doc/pg_repack.rst
%attr (755,root,root) %{pginstdir}/bin/pg_repack
%attr (755,root,root) %{pginstdir}/lib/pg_repack.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
  %endif
 %endif
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-1
- Update to 1.4.6

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.5-1
- Update to 1.4.5

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.4-1
- Update to 1.4.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu May 24 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Update to 1.4.3

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2, per #2791

* Wed Aug 16 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1, per #2364

* Fri Apr 28 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0, per #2364

* Wed Jun 1 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #1272

* Fri Feb 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3

* Wed Sep 9 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Tue May 20 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Fri Mar 23 2012 - Devrim Gunduz <devrim@gunduz.org> 1.1.7-1
- Initial packaging for PostgreSQL RPM Repository, based on the
  NTT spec, simplified and modified for PostgreSQL RPM compatibility.
- Cleaned up various rpmlint errors and warnings.
