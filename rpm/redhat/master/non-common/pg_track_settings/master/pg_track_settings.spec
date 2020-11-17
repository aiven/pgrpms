%global debug_package %{nil}
%global sname pg_track_settings

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL extension to keep track of settings modification
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.1
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/rjuju/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/rjuju/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.0.1-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pg_track_settings is a small extension that helps you keep track of
postgresql settings configuration.

It provides a function (pg_track_settings_snapshot()), that must be
called regularly. At each call, it will store the settings that have
been changed since last call. It will also track the postgresql
start time if it's different from the last one.

This extension tracks both overall settings (the pg_settings view)
and overloaded settings (the pg_db_role_setting table).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

#Avoid conflict with some other README file:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 6 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Switch to pgdg-srpm-macros

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1.1
- Rebuild against PostgreSQL 11.0

* Sun Jul 15 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-2
- Update for 9.5 doc layout.

* Thu Jul 23 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
