Summary:	Reliable PostgreSQL Backup & Restore
Name:		pgbackrest
Version:	1.16
Release:	1%{?dist}
License:	MIT
Group:		Applications/Databases
Url:		http://www.pgbackrest.org/
Source0:	https://github.com/pgbackrest/pgbackrest/archive/release/%{version}.tar.gz
Source1:	pgbackrest.conf.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	perl

%description
pgBackRest aims to be a simple, reliable backup and restore system that can
seamlessly scale up to the largest databases and workloads.

Instead of relying on traditional backup tools like tar and rsync, pgBackRest
implements all backup features internally and uses a custom protocol for
communicating with remote systems. Removing reliance on tar and rsync allows
for better solutions to database-specific backup challenges. The custom remote
protocol allows for more flexibility and limits the types of connections that
are required to perform a backup which increases security.

%prep
%setup -q -n %{name}-release-%{version}

%build

%install
install -D -d -m 0755 %{buildroot}%{perl_vendorlib} %{buildroot}%{_bindir}
install -D -d -m 0700 %{buildroot}/%{_sharedstatedir}/%{name}
install -D -d -m 0700 %{buildroot}/var/log/%{name}
install -D -d -m 0700 %{buildroot}/var/spool/%{name}
install -D -d -m 0755 %{buildroot}%{_sysconfdir}
install %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf
%{__cp} -a lib/*       %{buildroot}%{perl_vendorlib}/
%{__cp} -a bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%defattr(-,root,root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{_bindir}/%{name}
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{name}.conf
%{perl_vendorlib}/pgBackRest/
%attr(-,postgres,postgres) /var/log/%{name}
%attr(-,postgres,postgres) %{_sharedstatedir}/%{name}
%attr(-,postgres,postgres) /var/spool/%{name}

%changelog
* Fri Mar 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.16-1
- Update to 1.16

* Wed Feb 8 2017 - Devrim Gündüz <devrim@gunduz.org> 1.13-1
- Update to 1.13

* Thu Dec 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.12-1
- Update to 1.12

* Thu Nov 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.11-1
- Update to 1.11

* Tue Nov 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.10-1
- Update to 1.10

* Thu Nov 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Update to 1.09
- Install default conf file, per David Steele.
- Install default directories, per David Steele.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.08-1
- Update to 1.08

* Fri Aug 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Fri May 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial packaging for PostgreSQL RPM Repository

