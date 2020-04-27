%global sname check_pgbackrest

%global		_tag REL1_8

Name:		nagios-plugins-pgbackrest
Version:	1.8
Release:	1%{dist}
Summary:	pgBackRest backup check plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/%{_tag}.tar.gz
BuildArch:	noarch
Requires:	perl-JSON
Requires:	perl-Net-SFTP-Foreign
Requires:	perl-Data-Dumper
Requires:	nagios-plugins
Provides:	%{name} = %{version}
Obsoletes:	check_pgbackrest = 1.7

%description
check_pgbackrest is designed to monitor pgBackRest backups from Nagios.

%prep
%setup -q -n %{sname}-%{_tag}

%build

%install
%{__install} -D -p -m 0755 %{sname} %{buildroot}/%{_libdir}/nagios/plugins/%{name}

%files
%defattr(-,root,root,0755)
%{_libdir}/nagios/plugins/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README LICENSE
%else
%doc README
%license LICENSE
%endif

%changelog
* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> - 1.8-1
- Update to 1.8

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-2
- Various updates from Stefan Fercot:
 - Add missing dependencies
 - Rename package
 - Remove PostgreSQL dependency

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-1
- Initial version
