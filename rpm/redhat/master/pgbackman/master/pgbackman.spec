%global pbm_owner pgbackman
%global pbm_group pgbackman
%{!?pybasever: %global pybasever %(python -c "import sys;print(sys.version[0:3])")}
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	PostgreSQL backup manager
Name:		pgbackman
Version:	1.2.0
Release:	1%{?dist}
License:	GPLv3
Url:		http://www.pgbackman.org/
Source0:	https://github.com/rafaelma/%{name}/archive/%{version}.tar.gz
BuildArch:	noarch
Requires:	python-psycopg2 python-argparse at cronie python-setuptools shadow-utils logrotate

%description
PgBackMan is a tool for managing PostgreSQL logical backups created
with pg_dump and pg_dumpall.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup
servers topology.

It also manages role and database configuration information when
creating a backup of a database. This information is necessary to
ensure a 100% restore of a logical backup of a database and the
elements associated to it.

%prep
%setup -q

%build
python2 setup.py build

%install
python2 setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}/var/lib/%{name}
touch %{buildroot}/var/log/%{name}/%{name}.log

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL README.md
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/
%{python_sitelib}/%{name}/
%{_bindir}/%{name}*
%{_sysconfdir}/init.d/%{name}*
%{_sysconfdir}/logrotate.d/%{name}*
%{_datadir}/%{name}/*
/var/log/%{name}/*
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/%{name}/pgbackman_alerts.template
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(700,%{pbm_owner},%{pbm_group}) %dir /var/lib/%{name}
%attr(755,%{pbm_owner},%{pbm_group}) %dir /var/log/%{name}
%attr(600,%{pbm_owner},%{pbm_group}) %ghost /var/log/%{name}/%{name}.log

%pre
groupadd -f -r pgbackman >/dev/null 2>&1 || :
useradd -M -N -g pgbackman -r -d /var/lib/pgbackman -s /bin/bash \
	-c "PostgreSQL Backup Manager" pgbackman >/dev/null 2>&1 || :

%changelog
* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Fri Oct 30 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Fri Oct 30 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0
- Remove patch, it is now in upstream.
- Fix an rpmlint warning.

* Thu Oct 23 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-3
- Add a patch to support Fedora.

* Mon Jun 30 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-2
- Convert spaces to tabs in spec file
- Fix changelog date
- Update Source0 line with full URL
- Fix setup line, to match with tarball name.

* Mon Jun 23 2014 - Rafael Martinez Guerrero <rafael@postgresql.org.es> 1.0.0-1
- New release 1.0.0
