%global debug_package %{nil}
%global pgmajorversion 91
%global pgpoolinstdir /usr/pgpool-9.1/
%global pginstdir /usr/pgsql-9.1
%global sname pgpool-ha
%global ocfdir /usr/lib/ocf/resource.d/heartbeat/

Summary:	OCF style Resource Agent for pgpool-II
Name:		%{sname}
Version:	2.2
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://www.pgpool.net
Source0:	http://www.pgpool.net/download.php?f=%{sname}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	resource-agents, pgpool-II-%{pgmajorversion}

%description
Pgpool-HA combines pgpool with heartbeat. Pgpool is a replication
server of PostgreSQL and makes reliability, but the pgpool server is
always a single point failure.  Pgpool-HA uses heartbeat to eliminate
this.

%prep
%setup -q -n %{sname}-%{version}

%build
./configure.sh --with-pgpool=%{pgpoolinstdir} --with-pgsql=%{pginstdir} --with-ocf=%{ocfdir}
make %{?smp_flags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p -m 755 %{buildroot}%{ocfdir}
%{__install} -m 755 pgpool %{buildroot}%{ocfdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README ChangeLog
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif

%{ocfdir}/pgpool

%changelog
* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 2.2-2
- Cosmetic updates for unified spec file.

* Tue Sep 30 2014 Devrim GUNDUZ <devrim@gunduz.org> 2.2-1
- Update to 2.2
- Trim changelog
