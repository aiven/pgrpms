Summary:	PostgreSQL monitoring template for Zabbix
Name:		pg_monz
Version:	2.2
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/pg-monz/%{name}/
Source0:	https://github.com/pg-monz/%{name}/archive/2.2.tar.gz

Requires:	zabbix-agent >= 2.0 zabbix-sender >= 2.0 bc
Requires:	postgresql
BuildArch:	noarch

%global		_pgmonzdir	%{_datadir}/%{name}

%description
pg_monz enables various types of monitoring of PostgreSQL such as alive,
resource, performance, etc. It supports some constitution patterns which
includes single PostgreSQL pattern, HA pattern with Streaming Replication
and load balancing pattern with pgpool-II. You can use pg_monz for auto
recovery at the time of PostgreSQL system troubles, monitoring long-term
changes in PostgreSQL system status, and so on.

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_pgmonzdir}
%{__cp} -rp pg_monz/* %{buildroot}%{_pgmonzdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc quick-install.txt README-en.md README.md
%license LICENSE
%dir %{_pgmonzdir}
%attr(644,root,root) %{_pgmonzdir}/*

%changelog
* Thu Sep 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2-1
- Initial packaging for PostgreSQL RPM repository.
