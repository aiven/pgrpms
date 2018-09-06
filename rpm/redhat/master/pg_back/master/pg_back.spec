Name:           pg_back
Version:        1.6
Release:        1%{?dist}
Summary:        Simple backup script for PostgreSQL

License:        BSD
Group:          Applications/Databases
URL:            https://github.com/orgrim/%{name}
Source0:        https://github.com/orgrim/%{name}/archive/v%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_back is a simple backup script for PostgreSQL.

pg_back uses pg_dumpall to dump roles and tablespaces, pg_dump to dump
each selected database to a separate file. The custom format of pg_dump
is used by default.

A configuration file, by default /etc/postgresql/pg_back.conf, can hold
the configuration to automate the backup. All options can be overridden
on the command line.

%prep
%setup -q

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__install} -m 755 %{name} %{buildroot}/%{_bindir}
%{__install} -m 644 %{name}.conf %{buildroot}/%{_sysconfdir}/%{name}/

%files
%doc README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/%{name}

%changelog
* Thu Sep 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6-1
- Update to 1.6

* Mon Mar 12 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5

* Tue Mar 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Initial packaging for PostgreSQL RPM repository
