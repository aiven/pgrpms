%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:		temboard-agent
Version:	1.2
Release:	1%{?dist}.1
Summary:	PostgreSQL Remote Control agent

License:	PostgreSQL
URL:		http://temboard.io/
Source0:	https://github.com/dalibo/%{name}/archive/%{version}.tar.gz
%if %{systemd_enabled}
Source2:	%{name}.service
%else
Source1:	%{name}.init
Requires:	python-argparse python-logutils
%endif
Patch1:		%{name}.conf.patch

BuildArch:	noarch

BuildRequires:	python-setuptools
Requires:	openssl
Requires:	openssl /usr/sbin/useradd /usr/sbin/groupadd

%description
temBoard agent is a Python2 service designed to run along PostgreSQL,
exposing a REST API to implement various management tasks on PostgreSQL
instance. See http://temboard.io/ for the big picture.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%build
%{__python} setup.py build

%pre
# This comes from the PGDG rpm for PostgreSQL server. We want temboard to run
# under the same user as PostgreSQL
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%install
PATH=$PATH:%{buildroot}%{python_sitelib}/%{name}
%{__python} setup.py install --root=%{buildroot}
# config file
%{__install} -d -m 755 %{buildroot}/%{_sysconfdir}
%{__install} -d -m 750 %{buildroot}/%{_sysconfdir}/%{name}
%{__install} -m 600 %{buildroot}%{_datadir}/%{name}/%{name}.conf %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
%{__install} -m 644 %{buildroot}%{_datadir}/%{name}/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
%{__install} -d %{buildroot}%{_initrddir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__rm} -f %{buildroot}/usr/lib/systemd/system/%{name}.service
%endif

# log directory
%{__install} -d %{buildroot}/var/log/%{name}
# work directory
%{__install} -d %{buildroot}/var/lib/%{name}/main
# pidfile directory
%{__install} -d %{buildroot}/var/run/%{name}
%{__install} -m 600 /dev/null %{buildroot}/%{_sysconfdir}/%{name}/users

%post
# auto-signed SSL cert. building
openssl req -new -x509 -days 365 -nodes -out %{_sysconfdir}/pki/tls/certs/%{name}.pem -keyout %{_sysconfdir}/pki/tls/private/%{name}.key -subj "/C=XX/ST= /L=Default/O=Default/OU= /CN= " >> /dev/null 2>&1
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{name}.service
   %endif
   %else
   %systemd_post %{name}.service
   %tmpfiles_create
   %endif
  %else
   chkconfig --add %{name}
  %endif
fi

%files
%config(noreplace) %attr(-,postgres,postgres) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{python_sitelib}/*
%{_datadir}/%{name}/*
%{_bindir}/%{name}*

%if 0%{systemd_enabled}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%attr(-,postgres,postgres) /var/log/%{name}
%attr(-,postgres,postgres) /var/lib/%{name}
%config(noreplace) %attr(0600,postgres,postgres) %{_sysconfdir}/%{name}/users

%preun
if [ $1 -eq 0 ] ; then
 %if %{systemd_enabled}
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
 %else
	/sbin/service %{name} condstop >/dev/null 2>&1
	chkconfig --del %{name}
 %endif
fi


%postun
%if %{systemd_enabled}
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
	/sbin/service %{name} condrestart >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %{systemd_enabled}
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
 %else
	 /sbin/service %{name} condrestart >/dev/null 2>&1
 %endif
fi

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against PostgreSQL 11.0

* Fri Mar 16 2018 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2
- Rework on the spec file: Add Fedora and SLES support, use more macros,
  fix Patch1, reorganize BR and Requires, rpmlint fixes, and multiple other fixes.

* Wed Nov 8 2017 Julien Tachoires <julmon@gmail.com> - 1.1-1
- Handle systemd service on uninstall
- Build auto-signed SSL certs
- Set up users file as a config file
- Remove centos 5 support

* Mon Jul 4 2016 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 0.0.1-1
- Initial release
