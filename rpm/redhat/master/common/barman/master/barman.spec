%if 0%{?fedora} && 0%{?fedora} > 27
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%global __python_ver python3
BuildRequires:	python3
Requires:	python3
%endif

%if 0%{?rhel} && 0%{?rhel} > 7
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%global __python_ver python3
BuildRequires:	python36
Requires:	python36
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%global __python_ver python
BuildRequires:	python
Requires:	python
%endif

%if 0%{?suse_version} >= 1315
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%global __python_ver python2
%endif

%global pybasever %(%{__ospython} -c "import sys; print(sys.version[:3])")
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python_sitearch %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
  %global pybasever 2.7
%endif
%endif

Summary:	Backup and Recovery Manager for PostgreSQL
Name:		barman
Version:	2.10
Release:	2%{?dist}
License:	GPLv3
Url:		https://www.pgbarman.org/
Source0:	http://downloads.sourceforge.net/project/pgbarman/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.cron
Patch0:		%{name}-no-connection-from-backupinfo.patch
BuildArch:	noarch
BuildRequires:	%{__python_ver}-setuptools
Requires:	/usr/sbin/useradd rsync >= 3.0.4
Requires:	%{__python_ver}-barman = %{version}

%description
Barman (Backup and Recovery Manager) is an open-source administration tool for
disaster recovery of PostgreSQL servers written in Python. It allows your
organization to perform remote backups of multiple servers in business
critical environments to reduce risk and help DBAs during the recovery phase.

Barman is distributed under GNU GPL 3 and maintained by 2ndQuadrant.

%package -n barman-cli
Summary:	Client Utilities for Barman, Backup and Recovery Manager for PostgreSQL
Requires:	%{__python_ver}-barman = %{version}
%description -n barman-cli
Client utilities for the integration of Barman in PostgreSQL clusters.

%package -n %{__python_ver}-barman
Summary:	The shared libraries required for Barman family components
Requires:	%{__python_ver}-setuptools %{__python_ver}-psycopg2 >= 2.4.2
%if 0%{?suse_version} >= 1315
Requires:	python-dateutil
%endif
%if 0%{?rhel} || 0%{?fedora}
Requires:	%{__python_ver}-argh >= 0.21.2, %{__python_ver}-argcomplete
Requires:	%{__python_ver}-dateutil
%endif

%description -n %{__python_ver}-barman
Python libraries used by Barman.

%prep
%setup -n barman-%{version}%{?extra_version:%{extra_version}} -q
%patch0 -p1

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
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
%{_bindir}/barman-cloud-wal-archive
%doc %{_mandir}/man1/barman-cloud*
%doc %{_mandir}/man1/barman-wal*

%files -n %{__python_ver}-barman
%defattr(-,root,root)
%doc NEWS README.rst
%{python_sitelib}/%{name}-%{version}%{?extra_version:%{extra_version}}-py%{pybasever}.egg-info
%{python_sitelib}/%{name}/

%changelog
* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 2.10-2
- Fix SLES 12 dependency.

* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 2.10-1
- Update to 2.10, per changes described at:
  https://www.pgbarman.org/barman-2-10-released/#release-notes
- Add a temp patch, per https://redmine.postgresql.org/issues/4992#note-2
- Relax SLES 12 dependencies. Per #4910

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-2
- Un-break RHEL 6 packages. Per https://redmine.postgresql.org/issues/4767

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Wed May 15 2019 Marco Nenciarini <marco.nenciarini@2ndquadrant.it> 2.8-1
- New upstream version 2.8
- Add python3-barman and barman-cli binaries
- Build with python3 on FC > 27 and RHEL >= 8

* Sun Mar 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.7-1
- Update to 2.7

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6-1
- Update to 2.6

* Sat Dec 1 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5-2
- Fix RHEL 6 builds

* Fri Nov 16 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5-1
- Update to 2.5

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4-1.1
- Rebuild against PostgreSQL 11.0

* Wed Jun 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4, per #3402

- Perform a cleanup in th spec file, use macros for some binaries, remove
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
