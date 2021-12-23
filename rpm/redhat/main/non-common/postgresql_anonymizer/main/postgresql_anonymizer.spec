%global sname postgresql_anonymizer

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Anonymization & Data Masking for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.9.0
Release:	3%{?dist}
License:	PostgreSQL
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz
URL:		https://gitlab.com/dalibo/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	ddlx_%{pgmajorversion}

%if 0%{?suse_version} >= 1315
Requires:	python3-Faker
%else
Requires:	python3-faker
%endif
Obsoletes:	%{sname}%{pgmajorversion} < 0.7.1-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

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
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.md
%else
%license LICENSE.md
%endif
%defattr(644,root,root,755)
%{pginstdir}/bin/pg_dump_anon
%{pginstdir}/lib/anon.so
%{pginstdir}/share/extension/anon/*
%{pginstdir}/share/extension/anon.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/anon*.bc
   %{pginstdir}/lib/bitcode/anon/*.bc
  %endif
 %endif
%endif

%changelog
* Thu Dec 23 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-3
- Fix SLES dependency name

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-2
- Add SLES support.

* Sun Jul 4 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-1
- Update to 0.9.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-2
- Remove pgxs patches, and export PATH instead.

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-1
- Update to 0.8.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Sep 29 2020 Devrim Gündüz <devrim@gunduz.org> 0.7.1-1
- Update to 0.7.1

* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> 0.6.0-1
- Update to 0.6.0

* Sat Nov 9 2019 Devrim Gündüz <devrim@gunduz.org> 0.5.0-1
- Update to 0.5.0

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-2
- Require -contrib subpackage for tsm_system_rows extension. Per
  Damien: https://redmine.postgresql.org/issues/4861

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-1
- Update to 0.4.1

* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1.1
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Wed Aug 14 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0
- Add ddlx dependency

* Tue Nov 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.2.1-1
- Initial packaging for PostgreSQL RPM Repository
