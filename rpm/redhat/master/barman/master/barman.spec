%if 0%{?rhel} == 7
  %global pybasever 2.7
 %else
  %if 0%{?fedora}>= 25
    %global pybasever 2.7
  %else
    %global pybasever 2.6
    %endif
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
  %global pybasever 2.7
%endif
%endif

%global __python_ver python

%{!?pybasever: %global pybasever %(%{__python} -c "import sys;print(sys.version[0:3])")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Backup and Recovery Manager for PostgreSQL
Name:		barman
Version:	2.3
Release:	1%{?dist}
License:	GPLv3
Group:		Applications/Databases
Url:		http://www.pgbarman.org/
Source0:	http://downloads.sourceforge.net/project/pgbarman/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.cron
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	python-abi = %{pybasever}, %{__python_ver}-psycopg2 >= 2.4.2, %{__python_ver}-argh >= 0.21.2, %{__python_ver}-argcomplete, %{__python_ver}-dateutil
Requires:	/usr/sbin/useradd
Requires:	rsync >= 3.0.4

%description
Barman (Backup and Recovery Manager) is an open-source
administration tool for disaster recovery of PostgreSQL
servers written in Python.
It allows your organisation to perform remote backups of
multiple servers in business critical environments to
reduce risk and help DBAs during the recovery phase.

Barman is distributed under GNU GPL 3 and maintained
by 2ndQuadrant.

%prep
%setup -n barman-%{version}%{?extra_version:%{extra_version}} -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
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
useradd -M -n -g barman -r -d /var/lib/barman -s /bin/bash \
	-c "Backup and Recovery Manager for PostgreSQL" barman >/dev/null 2>&1 || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL NEWS README.rst
%{python_sitelib}/%{name}-%{version}%{?extra_version:%{extra_version}}-py%{pybasever}.egg-info
%{python_sitelib}/%{name}/
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

%changelog
* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3, per #2682.
- Perform a cleanup in th spec file, use macros for some binaries, remove
  RHEL 5 references, and remove excessive macro usage in version and release
  number.
- Use separate sources for logrotate and cron files.

* Tue Jul 18 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Fri Jan 6 2017 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Tue Sep 27 2016 - Gabriele Bartolini <gabriele.bartolini@2ndquadrant.it> 2.0-1
- New release 2.0-1
- Trim changelog for releases 1.X
