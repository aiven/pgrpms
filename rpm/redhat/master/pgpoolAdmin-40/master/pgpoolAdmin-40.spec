%global pgpoolmajorversion 4.0

%global	_pgpoolAdmindir	%{_datadir}/%{name}

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

Summary:	PgpoolAdmin - web-based pgpool administration
Name:		pgpoolAdmin
Version:	%{pgpoolmajorversion}.1
Release:	1%{?dist}
License:	BSD
URL:		https://pgpool.net

Source0:	https://www.pgpool.net/download.php?f=%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Requires:	php, php-pgsql, php-posix, webserver
Requires:	webserver
Requires:	pgpool-II-%{pgmajorversion} >= %{version}

BuildArch:	noarch

%if %{systemd_enabled}
BuildRequires:	systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

Patch1:		%{name}-pg%{pgmajorversion}-conf.patch

%description
The pgpool Administration Tool is management tool of pgpool-II. It is
possible to monitor, start, stop pgpool and change settings of pgpool-II.

%prep
%setup -q
%patch1 -p0
%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_pgpoolAdmindir}
%{__install} -d %{buildroot}%{_pgpoolAdmindir}/conf
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 644 *.php %{buildroot}%{_pgpoolAdmindir}
%{__cp} -a  doc/ images/ install/ lang/ libs/ templates/ screen.css %{buildroot}%{_pgpoolAdmindir}
%{__install} -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}/
%{__ln_s}  ../../../..%{_sysconfdir}/%{name}/pgmgt.conf.php %{buildroot}%{_pgpoolAdmindir}/conf/pgmgt.conf.php

if [ -d %{_sysconfdir}/httpd/conf.d/ ]
then
	%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
	%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
fi

%post
%if %{systemd_enabled}
	systemctl reload httpd.service > /dev/null 2>&1
%else
	/sbin/service httpd reload > /dev/null 2>&1
%endif
	chgrp apache /var/log/pgpool-II-%{pgmajorversion}
	chgrp apache /var/run/pgpool-II-%{pgmajorversion}
	chmod g+rwx /var/log/pgpool-II-%{pgmajorversion}
	chmod g+rwx /var/run/pgpool-II-%{pgmajorversion}

%postun
%if %{systemd_enabled}
	systemctl reload httpd.service
%else
	/sbin/service httpd reload > /dev/null 2>&1
%endif
	chmod g+rwx /var/log/pgpool-II-%{pgmajorversion}
	chmod g+rwx /var/run/pgpool-II-%{pgmajorversion}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,apache,apache,0755)
%doc README README.euc_jp
%dir %{_pgpoolAdmindir}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0755,root,root) %{_pgpoolAdmindir}/*.php
%{_pgpoolAdmindir}/conf
%{_pgpoolAdmindir}/doc
%{_pgpoolAdmindir}/images
%{_pgpoolAdmindir}/install
%{_pgpoolAdmindir}/lang
%{_pgpoolAdmindir}/libs
%{_pgpoolAdmindir}/templates
%{_pgpoolAdmindir}/screen.css

%changelog
* Wed Dec 19 2018 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Initial packaging for pgpoolAdmin 4.0
