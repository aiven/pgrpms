%global debug_package %{nil}
%global sname pgbouncer_fdw

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	pgbouncer Foreign Data Wrapper
Name:		%{sname}_%{pgmajorversion}
Version:	0.4
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/CrunchyData/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/CrunchyData/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	pgbouncer >= 1.10

Obsoletes:	%{sname}%{pgmajorversion} < 0.2-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgbouncer_fdw provides a direct SQL interface to the pgbouncer SHOW commands.
It takes advantage of the dblink_fdw feature to provide a more typical,
table-like interface to the current status of your pgbouncer server(s).
This makes it easier to set up monitoring or other services that require
direct access to pgbouncer statistics.

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
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH  %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE.txt
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 0.4-1
- Update to 0.4

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.3-2
- Remove pgxs patches, and export PATH instead.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 0.3-1
- Update to 0.3

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Sep 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.2-1
- Initial packaging for PostgreSQL RPM Repository
