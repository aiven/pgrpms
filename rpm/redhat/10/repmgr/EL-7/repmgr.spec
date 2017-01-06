%global pgmajorversion 10
%global pgpackageversion 10
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname repmgr
%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%global _varrundir %{_localstatedir}/run/%{sname}

Name:		%{sname}%{pgmajorversion}
Version:	3.2.1
Release:	1%{?dist}
Summary:	Replication Manager for PostgreSQL Clusters
License:	GPLv3
URL:		http://www.repmgr.org
Source0:	http://repmgr.org/download/%{sname}-%{version}.tar.gz
Source1:	repmgr-%{pgpackageversion}.service
Source2:	repmgr.init
Source3:	repmgr.sysconfig
Patch0:		repmgr-makefile-pgxs.patch
Patch1:		repmgr.conf.sample.patch

%if %{systemd_enabled}
BuildRequires:		systemd
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
# This is for older spec files (RHEL <= 6)
Group:		Applications/Databases
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
BuildRequires:	postgresql%{pgmajorversion}, postgresql%{pgmajorversion}-devel
BuildRequires:	libxslt-devel, pam-devel, openssl-devel, readline-devel
Requires:	postgresql%{pgmajorversion}-server

%description
repmgr is an open-source tool suite to manage replication and failover in a
cluster of PostgreSQL servers. It enhances PostgreSQL's built-in hot-standby
capabilities with tools to set up standby servers, monitor replication, and
perform administrative tasks such as failover or manual switchover operations.

repmgr has provided advanced support for PostgreSQL's built-in replication
mechanisms since they were introduced in 9.0, and repmgr 2.0 supports all
PostgreSQL versions from 9.0 to 9.5. With further developments in replication
functionality such as cascading replication, timeline switching and base
backups via the replication protocol, the repmgr team has decided to use
PostgreSQL 9.3 as the baseline version for repmgr 3.0, which is a substantial
rewrite of the existing repmgr code and which will be developed to support
future PostgreSQL versions.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
%if %{systemd_enabled}
# Use new %%make_install macro:
USE_PGXS=1 %make_install  DESTDIR=%{buildroot}
%else
# Use older version
USE_PGXS=1 %{__make} install  DESTDIR=%{buildroot}
%endif
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
# Install sample conf file
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/
install -m 644 repmgr.conf.sample %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf

%if %{systemd_enabled}
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 postgres postgres -
EOF

%else
install -d %{buildroot}%{_sysconfdir}/init.d
install -m 755 %{SOURCE2}  %{buildroot}%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
# Create the sysconfig directory and config file:
install -d -m 700 %{buildroot}%{_sysconfdir}/sysconfig/%{sname}/
install -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{sname}/%{sname}-%{pgpackageversion}
%endif

%pre
if [ ! -x /var/log/repmgr ]
then
	%{__mkdir} -m 700 /var/log/repmgr
	%{__chown} -R postgres: /var/log/repmgr
fi

%post
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%tmpfiles_create
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{sname}-%{pgpackageversion}
%endif
if [ ! -x %{_varrundir} ]
then
	%{__mkdir} -m 700 %{_varrundir}
	%{__chown} -R postgres: %{_varrundir}
fi

%postun -p /sbin/ldconfig

%files
%if %{systemd_enabled}
%doc CREDITS HISTORY README.md
%license COPYRIGHT LICENSE
%else
%defattr(-,root,root,-)
%doc CREDITS HISTORY README.md LICENSE COPYRIGHT
%endif
%dir %{pginstdir}/bin
%dir %{_sysconfdir}/%{sname}/%{pgpackageversion}/
%config(noreplace) %{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf
%{pginstdir}/bin/repmgr
%{pginstdir}/bin/repmgrd
%{pginstdir}/lib/repmgr_funcs.so
%{pginstdir}/share/contrib/repmgr.sql
%{pginstdir}/share/contrib/repmgr_funcs.sql
%{pginstdir}/share/contrib/uninstall_repmgr.sql
%{pginstdir}/share/contrib/uninstall_repmgr_funcs.sql
%if %{systemd_enabled}
%ghost %{_varrundir}
%{_tmpfilesdir}/%{name}.conf
%attr (644, root, root) %{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
%config(noreplace) %attr (600,root,root) %{_sysconfdir}/sysconfig/%{sname}/%{sname}-%{pgpackageversion}
%endif

%changelog
* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1. Fixes #1897

* Fri Oct 7 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2. Fixes #1836

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.5-1
- Update to 3.1.5

* Fri May 20 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.3-1
- Update to 3.1.3

* Mon May 02 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.2-2
- Fix shell redirection in systemd service file (#1052)

* Tue Mar 8 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.1-2
- Don't overwrite config files on upgrade, save as .rpmnew instead (#1029, per
  report by Brett Maton)
- sysconfig file should not be installed executable (#1030)
- Fix RPM group name (#1030)
- systemd service file should not be executable (#1030)

* Thu Feb 25 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.1-1
- Upstream release 3.1.1

* Mon Feb 22 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-3
- Fix permissions of sysconfig file. Per #1004.

* Tue Feb 16 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-2
- Install correct sysconfig file, instead of init script. Per
  bug report from Brett Maton.

* Tue Jan 5 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-1
- Update to 3.0.3
- Apply various fixes to init script, and also add sysconfig
  file. Patch from Martín Marqués.
- Fix some rpmlint warnings.

* Mon Nov 9 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-2
- Ensure that /var/run/repmgr exists. Per Guillaume Lelarge.
- Switch to postgres user while running the deamon, instead of
  repmgr user. Per recent complaints from Guillaume and Justin King.

* Tue Oct 6 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Tue May 12 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Update description and some other minor places.
- More for creating unified spec file for all distros, and put
  back some stuff into conditionals. Also, use %%license macro
  only on newer releases.

* Fri May 1 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-4
- chown pid file dir and fix its path.
- Fix unit file

* Wed Apr 29 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-3
- Add %%license macro
- Omit obsoleted BuildRoot and Group macros.
- Use %%make_install macro
- Omit %%clean
- No need to cleanup buildroot during %%install
- Run ldconfig

* Tue Mar 24 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Add unit file/init script for repmgr. This spec file can be
  used on all platforms.
- Updated BR, per mock build.

* Thu Feb 19 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2, per changes described at:
  http://www.repmgr.org/release-notes-2.0.2.html

* Thu Mar 20 2014 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Tue Apr 3 2012 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-2
- Spec file fixes by Satoshi Nagayasu
- Updated patch0 and renamed it for better convenience.
- Replaced postgresql-devel dependency with postgresql, since
  pg_config is now in main package.

* Wed Oct 19 2011 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Initial packaging.
