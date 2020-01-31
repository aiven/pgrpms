%global		_tag REL1_7

Name:		check_pgbackrest
Version:	1.7
Release:	1%{dist}
Summary:	pgBackRest backup check plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{name}
Source0:	https://github.com/dalibo/%{name}/archive/%{_tag}.tar.gz
BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}
Requires:	nagios-plugins
Provides:	%{name} = %{version}

%description
check_pgbackrest is designed to monitor pgBackRest backups from Nagios.

%prep
%setup -q -n %{name}-%{_tag}

%build

%install
%{__install} -D -p -m 0755 %{name} %{buildroot}/%{_libdir}/nagios/plugins/%{name}

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
* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-1
- Initial version
