%global sname check_pgbackrest

%global		_tag REL1_7

Name:		check_pgbackrest
Version:	1.7
Release:	1%{dist}
Summary:	pgBackRest backup check plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/check_pgbackrest
Source0:	https://github.com/dalibo/check_pgbackrest/archive/REL1_7.tar.gz
BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}
Requires:	nagios-plugins
Provides:	%{sname} = %{version}

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
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README LICENSE
%else
%doc README
%license LICENSE
%endif

%changelog
* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7-1
- Initial version
