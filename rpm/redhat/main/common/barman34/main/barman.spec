%{expand: %%global pybasever %(echo `%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}

%global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	Backup and Recovery Manager for PostgreSQL
Name:		barman
Version:	3.4.1
Release:	1%{?dist}
License:	GPLv3
Url:		https://www.pgbarman.org/
Source0:	https://github.com/EnterpriseDB/%{name}/archive/refs/tags/release/%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.cron
BuildArch:	noarch
BuildRequires:	python2-setuptools
Requires:	/usr/sbin/useradd rsync >= 3.0.4
Requires:	python2-barman = %{version}

BuildRequires:	python2-devel
Requires:	python2

%description
Barman (Backup and Recovery Manager) is an open-source administration tool for
disaster recovery of PostgreSQL servers written in Python. It allows your
organization to perform remote backups of multiple servers in business
critical environments to reduce risk and help DBAs during the recovery phase.

Barman is distributed under GNU GPL 3 and maintained by EnterpriseDB.

%package -n barman-cli
Summary:	Client Utilities for Barman, Backup and Recovery Manager for PostgreSQL
Requires:	python2-barman = %{version}
%description -n barman-cli
Client utilities for the integration of Barman in PostgreSQL clusters.

%package -n python2-barman
Summary:	The shared libraries required for Barman family components
Requires:	python-setuptools python2-psycopg2 >= 2.8.6
Requires:	python-dateutil

%description -n python2-barman
Python libraries used by Barman.

%prep
%setup -q -n barman-release-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/bash_completion.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/cron.d/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/barman.d/
%{__mkdir} -p %{buildroot}/var/lib/barman
%{__mkdir} -p %{buildroot}/var/log/barman
%{__install} -pm 644 doc/barman.conf %{buildroot}%{_sysconfdir}/barman.conf
%{__install} -pm 644 doc/barman.d/* %{buildroot}%{_sysconfdir}/barman.d/
%{__install} -pm 644 scripts/barman.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/barman
%{__install} -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/barman
%{__install} -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.d/barman
touch %{buildroot}/var/log/barman/barman.log

%pre
groupadd -f -r barman >/dev/null 2>&1 || :
useradd -M -g barman -r -d /var/lib/barman -s /bin/bash \
	-c "Backup and Recovery Manager for PostgreSQL" barman >/dev/null 2>&1 || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS README.rst
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.gz
%doc %{_mandir}/man5/%{name}.5.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/barman.d/
%attr(700,barman,barman) %dir /var/lib/%{name}
%attr(755,barman,barman) %dir /var/log/%{name}
%attr(600,barman,barman) %ghost /var/log/%{name}/%{name}.log

%files -n barman-cli
%defattr(-,root,root)
%doc NEWS README.rst
%{_bindir}/barman-wal-archive
%{_bindir}/barman-wal-restore
%{_bindir}/barman-cloud-backup
%{_bindir}/barman-cloud-backup-delete
%{_bindir}/barman-cloud-backup-keep
%{_bindir}/barman-cloud-backup-show
%{_bindir}/barman-cloud-check-wal-archive
%{_bindir}/barman-cloud-wal-archive
%{_bindir}/barman-cloud-backup-list
%{_bindir}/barman-cloud-restore
%{_bindir}/barman-cloud-wal-restore
%doc %{_mandir}/man1/barman-cloud*
%doc %{_mandir}/man1/barman-wal*

%files -n python2-barman
%defattr(-,root,root)
%doc NEWS README.rst
%{python_sitelib}/%{name}-%{version}%{?extra_version:%{extra_version}}-py%{pybasever}.egg-info
%{python_sitelib}/%{name}/

%changelog
* Fri May 26 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Package 3.4.X for SLES 12 only. The Python version in SLES 12
  (3.4) is not sufficient for Barman, which requires at least 3.6.
