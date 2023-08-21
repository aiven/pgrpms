%global sname check_pgbackrest

%global		_tag REL2_3

Name:		nagios-plugins-pgbackrest
Version:	2.3
Release:	2PGDG%{dist}
Summary:	pgBackRest backup check plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/pgstef/%{sname}
Source0:	https://github.com/pgstef/%{sname}/archive/%{_tag}.tar.gz
BuildArch:	noarch
Requires:	perl-JSON
Requires:	nagios-plugins

%if 0%{?rhel} && 0%{?rhel} >= 8
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
%else
Requires:	perl-Data-Dumper
%endif
Provides:	%{name} = %{version}
Obsoletes:	check_pgbackrest = 1.7

%description
check_pgbackrest is designed to monitor pgBackRest backups from Nagios.

%prep
%setup -q -n %{sname}-%{_tag}

%build

%install
%{__install} -D -p -m 0755 %{sname} %{buildroot}/%{_libdir}/nagios/plugins/%{sname}

%files
%defattr(-,root,root,0755)
%{_libdir}/nagios/plugins/%{sname}
%doc README
%license LICENSE

%changelog
* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.3-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Tue May 31 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Mon Dec 6 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2-1
- Update to 2.2

* Thu Sep 30 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1-2
- Update URLs, per Stefan.

* Wed Sep 29 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Update to 2.1

* Thu Feb 11 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0-2
- Remove unused	dependencies, per Stefan.

* Wed Feb 10 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Wed Dec 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.9-2
- Add weak dependencies for RHEL 8, per
  https://redmine.postgresql.org/issues/5381#note-2

* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.9-1
- Update to 1.9

* Mon Apr 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.8-2
- Fix plugin name, per #5381 and
  https://github.com/dalibo/check_pgbackrest/issues/7

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> - 1.8-1
- Update to 1.8

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-2
- Various updates from Stefan Fercot:
 - Add missing dependencies
 - Rename package
 - Remove PostgreSQL dependency

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-1
- Initial version
