%global	pgmajorversion 91
%global	_pgpoolAdmindir	%{_datadir}/%{name}

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

Summary:	PgpoolAdmin - web-based pgpool administration
Name:		pgpoolAdmin
Version:	3.5.3
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgpool.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://www.pgpool.net/download.php?f=%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Requires:	php >= 4.3.9
Requires:	php-pgsql >= 4.3.9
Requires:	webserver
Requires:	pgpool-II-%{pgmajorversion} >= %{version}

BuildArch:	noarch
BuildRequires:	httpd
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

Patch1:		%{name}-conf.patch

%description
The pgpool Administration Tool is management tool of pgpool-II. It is
possible to monitor, start, stop pgpool and change settings of pgpool-II.

%prep
%setup -q
%patch1 -p0
%build

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{_pgpoolAdmindir}
install -d %{buildroot}%{_pgpoolAdmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 *.php %{buildroot}%{_pgpoolAdmindir}
%{__cp} -a  doc/ images/ install/ lang/ libs/ templates/ screen.css %{buildroot}%{_pgpoolAdmindir}
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}/
ln -s ../../../..%{_sysconfdir}/%{name}/pgmgt.conf.php %{buildroot}%{_pgpoolAdmindir}/conf/pgmgt.conf.php

if [ -d %{_sysconfdir}/httpd/conf.d/ ]
then
	install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
	install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
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
* Mon Oct 24 2016 Devrim Gündüz <devrim@gunduz.org> 3.5.3-2
- Fix PG major version. Per #1882.

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> 3.5.3-1
- Update to 3.5.3

* Wed Feb 10 2016 Devrim Gündüz <devrim@gunduz.org> 3.5.0-1
- Update to 3.5.0
- Make sure that the right version of pgpool-II is picked up.

* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 3.4-1-2
- Use macro for PostgreSQL version.
- Cosmetic cleanup

* Thu Apr 9 2015 Devrim Gunduz <devrim@gunduz.org> 3.4-1-1
- Update to 3.4.1
- Update spec file so that it works with all distros.
- Change file ownership from nobody to apache.
- Update Apache conf file for Apache > 2.3
- Update patch0

* Thu Dec 10 2009 Devrim Gunduz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Mon Mar 23 2009 Devrim Gunduz <devrim@gunduz.org> 2.2-1
- Update to 2.2
- Update spec and patches so that pgpoolAdmin works against pgpool 2.2

* Sun Jun 15 2008 Devrim Gunduz <devrim@gunduz.org> 2.1-beta1-1
- Update to 2.1 beta1

* Tue Oct 16 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.0-9
- Fixed smarty error caused by wrong ownership
- Change php requires version for EL-4

* Thu Aug 16 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.0-8
- Fix ownership problem of pgmgmt.conf

* Thu Aug 16 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.0-7
- Fix httpd configuration file -- it was using wrong directory.

* Sat Jun 2 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.0-6
- Fixes for bugzilla review #229323

* Tue Feb 20 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.0-5
- Fixes for packaging guidelines of web apps.
- Fix ownership problems

* Mon Oct 02 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.0-4
- chgrp and chmod pgpool-II conf files so that apache can write it.
- Change file ownership from apache to nobody.

* Tue Sep 26 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.0-3
- Update patch1

* Tue Sep 26 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.0-2
- Fix file ownership
- Update patch1

* Tue Sep 26 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.0-1
- Initial build 
