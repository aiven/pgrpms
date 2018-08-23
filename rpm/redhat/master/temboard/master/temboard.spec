%global confdir %{_sysconfdir}/%{name}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:		temboard
Version:	1.2.1
Release:	1%{?dist}
Summary:	temBoard Web Interface

Group:		Applications/Databases
License:	PostgreSQL
URL:		http://temboard.io/
Source0:	https://github.com/dalibo/%{name}/archive/%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}-tmpfiles.d
Patch0:		%{name}-conf.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-setuptools
Requires:	python-tornado >= 3.2 python-sqlalchemy >= 0.9.8
Requires:	python-psycopg2 python-dateutil >= 1.5 openssl

BuildRequires:		systemd, systemd-devel
# We require this to be present for tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%endif
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
temBoard is a monitoring and remote control solution for PostgreSQL
This packages holds the web user interface

%prep
%setup -q -n %{name}-%{version}
%patch0 -p 0

%build
%{__python} setup.py build

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%install
PATH=$PATH:%{buildroot}%{python_sitelib}/%{name}
%{__python} setup.py install --root=%{buildroot}
# config file
%{__install} -d -m 755 %{buildroot}/%{_sysconfdir}
%{__install} -d -m 750 %{buildroot}/%{confdir}
%{__install} -m 640 %{buildroot}/usr/share/%{name}/quickstart/%{name}.conf %{buildroot}/%{confdir}/%{name}.conf
%{__install} -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
%{__install} -m 644 %{buildroot}/usr/share/%{name}/quickstart/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%{__install}  -d %{buildroot}%{_unitdir}
%{__install}  -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# log directory
%{__install} -d %{buildroot}/var/log/%{name}
# home directory
%{__install} -d %{buildroot}/var/lib/%{name}

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

%pre
# We want a system user and group to run the tornado webapp
groupadd -r %{name} >/dev/null 2>&1 || :
useradd -M -g %{name} -r -d /var/empty/%{name} -s /sbin/nologin \
    -c "temBoard Web UI" %{name} >/dev/null 2>&1 || :

%post
# auto-signed SSL cert. building
openssl req -new -x509 -days 365 -nodes -out %{_sysconfdir}/%{name}/%{name}.pem -keyout %{_sysconfdir}/%{name}/%{name}.key -subj "/C=XX/ST= /L=Default/O=Default/OU= /CN= " >> /dev/null 2>&1
%{__chown} %{name}:%{name} %{_sysconfdir}/%{name}/%{name}.pem %{_sysconfdir}/%{name}/%{name}.key
# Systemd stuff:
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{name}.service
   %endif
   %else
   %systemd_post %{name}.service
   %tmpfiles_create
   %endif
fi

%files
%attr(-,%{name},%{name}) /var/lib/%{name}
%attr(-,%{name},%{name}) /var/log/%{name}
%config(noreplace) %attr(-,%{name},%{name}) %{confdir}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{python_sitelib}/*
%{_datadir}/%{name}/*
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf

%changelog
* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1

* Wed Mar 7 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2
- Various fixes to packaging, so that it works out of the box.

* Wed Nov 8 2017 Julien Tachoires <julmon@gmail.com> - 1.1-1
- Handling /var/lib/temboard directory
- Auto-signed SSL certs.
- Usage of a dedicated temboard config. file

* Fri Jul 15 2016 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 0.0.1-1
- Initial release
