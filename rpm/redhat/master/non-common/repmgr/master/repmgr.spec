%global sname repmgr
%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	5.2.1
Release:	1%{?dist}
Summary:	Replication Manager for PostgreSQL Clusters
License:	GPLv3
URL:		https://www.repmgr.org
Source0:	https://repmgr.org/download/%{sname}-%{version}.tar.gz
%if %{systemd_enabled}
Source1:	repmgr-pg%{pgmajorversion}.service
%else
Source2:	repmgr-pg%{pgmajorversion}.init
%endif
Source3:	repmgr-pg%{pgmajorversion}.sysconfig
Patch0:		repmgr-pg%{pgmajorversion}-conf.sample.patch
Patch1:		repmgr-pg%{pgmajorversion}-config-file-location.patch

%if %{systemd_enabled}
BuildRequires:          systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	libxslt-devel pam-devel openssl-devel readline-devel
BuildRequires:	libmemcached-devel libicu-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <= 5.2.0-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

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

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
%package devel
Summary:	Development header files of repmgr
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The repmgr-devel package contains the header files needed to compile C or C++
applications which will directly interact with repmgr.
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p1

export PG_CONFIG=%{pginstdir}/bin/pg_config
%configure

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
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
%{__install} -m 644 repmgr.conf.sample %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 postgres postgres -
EOF

%else
%{__install} -d %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
# Create the sysconfig directory and config file:
%{__install} -d -m 700 %{buildroot}%{_sysconfdir}/sysconfig/%{sname}/
%{__install} -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{sname}/%{sname}-%{pgpackageversion}
%endif

%pre
if [ ! -x /var/log/repmgr ]
then
	%{__mkdir} -m 700 /var/log/repmgr
	%{__chown} -R postgres: /var/log/repmgr
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
    %service_add_pre %{sname}-%{pgmajorversion}.service
   %endif
   %else
    %systemd_post %{sname}-%{pgmajorversion}.service
   %endif
  %else
   /sbin/chkconfig --add %{sname}-%{pgpackageversion}
  %endif
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
%{pginstdir}/lib/repmgr.so
%{pginstdir}/share/extension/repmgr.control
%{pginstdir}/share/extension/repmgr*sql
%if %{systemd_enabled}
%ghost %{_rundir}/%{sname}
%{_tmpfilesdir}/%{name}.conf
%attr (644, root, root) %{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
%config(noreplace) %attr (600,root,root) %{_sysconfdir}/sysconfig/%{sname}/%{sname}-%{pgpackageversion}
%endif
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
  %ifnarch ppc64 ppc64le
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
%files devel
%defattr(-,root,root,-)
%endif

%changelog
* Tue Dec 8 2020 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Oct 22 2020 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0

* Mon Apr 13 2020 - Devrim Gündüz <devrim@gunduz.org> 5.1.0-1
- Update to 5.1.0

* Wed Oct 16 2019 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.0.0

* Thu Jun 27 2019 - Devrim Gündüz <devrim@gunduz.org> 4.4.0-1
- Update to 4.4.0

* Fri Apr 12 2019 - Devrim Gündüz <devrim@gunduz.org> 4.3.0-2
- Fix tmpfilesd directory. Per https://redmine.postgresql.org/issues/4156

* Wed Apr 3 2019 - Devrim Gündüz <devrim@gunduz.org> 4.3.0-1
- Update to 4.3.0
- Fix https://redmine.postgresql.org/issues/3717. Patch from Ian
  Barwick.
- Fix https://redmine.postgresql.org/issues/3718. Patch from Ian
  Barwick.

* Sat Dec 22 2018 - Devrim Gündüz <devrim@gunduz.org> 4.2.0-2
- Fix path in tmpfiles.d drop-in file

* Tue Nov 6 2018 - Devrim Gündüz <devrim@gunduz.org> 4.2.0-1
- Update to 4.2.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Sep 6 2018 - Devrim Gündüz <devrim@gunduz.org> 4.1.1-1
- Update to 4.1.1, per #3623
- Add -devel subpackage for v11+

* Wed Aug 1 2018 - Devrim Gündüz <devrim@gunduz.org> 4.1.0-1
- Update to 4.1.0, per #3530

* Thu Jun 14 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.6-1
- Update to 4.0.6, per #3419

* Fri May 4 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.5-1
- Update to 4.0.5

* Mon Apr 16 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.4-1
- Update to 4.0.4, per #3264.

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.3-1
- Update to 4.0.3

* Thu Jan 18 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.2-1
- Update to 4.0.2

* Tue Jan 2 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1

* Tue Nov 21 2017 - Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0
- Remove patch0, not needed anymore.

* Sun Jun 11 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3.2-1
- Update to 3.3.2, per #2472 .

* Sun Apr 2 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1, per #2296 .

* Mon Mar 13 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3-2
- Fix quoting bug in sample conf file patch. Per report from Magnus.
  Fixes #2248.

* Fri Jan 6 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3-1
- Update to 3.3

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
