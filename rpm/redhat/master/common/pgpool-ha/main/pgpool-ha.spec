%global debug_package %{nil}
%global sname pgpool-ha
%global ocfdir /usr/lib/ocf/resource.d/heartbeat/

Summary:	OCF style Resource Agent for pgpool-II
Name:		%{sname}
Version:	3.0
Release:	1%{?dist}.1
License:	BSD
URL:		http://www.pgpool.net
Source0:	http://www.pgpool.net/download.php?f=%{sname}-%{version}.tar.bz2
Requires:	resource-agents

%description
Pgpool-HA combines pgpool with heartbeat. Pgpool is a replication
server of PostgreSQL and makes reliability, but the pgpool server is
always a single point failure.  Pgpool-HA uses heartbeat to eliminate
this.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p -m 755 %{buildroot}%{ocfdir}
%{__install} -m 755 pgpool.in %{buildroot}%{ocfdir}/pgpool

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md ChangeLog
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{ocfdir}/pgpool

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0-1.1
- Rebuild against PostgreSQL 11.0

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 2.2-2
- Cosmetic updates for unified spec file.

* Tue Sep 30 2014 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2
- Trim changelog
