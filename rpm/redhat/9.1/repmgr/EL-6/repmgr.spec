%global pgmajorversion 91
%global pgpackageversion 9.1
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname repmgr
%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%global _varrundir %{_localstatedir}/run/%{sname}

Name:           %{sname}%{pgmajorversion}
Version:        2.0.2
Release:        4%{?dist}
Summary:        Replication Manager for	PostgreSQL Clusters
License:        GPLv3
URL:            http://www.repmgr.org
Source0:        http://repmgr.org/download/%{sname}-%{version}.tar.gz
Source1:	repmgr-%{pgpackageversion}.service
Source2:	repmgr.init
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
%endif
BuildRequires:  postgresql%{pgmajorversion}, postgresql%{pgmajorversion}-devel
BuildRequires:	libxslt-devel, pam-devel, openssl-devel, readline-devel
Requires:       postgresql%{pgmajorversion}-server

%description
repmgr is a set of open source tools that helps DBAs and System
administrators manage a cluster of PostgreSQL databases..

By taking advantage of the Hot Standby capability introduced in
PostgreSQL 9, repmgr greatly simplifies the process of setting up and
managing database with high availability and scalability requirements.

repmgr simplifies administration and daily management, enhances
productivity and reduces the overall costs of a PostgreSQL cluster by:
  * monitoring the replication process;
  * allowing DBAs to issue high availability operations such as
switch-overs and fail-overs.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
USE_PGXS=1 %make_install  DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
# Install sample conf file
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/
install -m 644 repmgr.conf.sample %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf

%if %{systemd_enabled}
install -d %{buildroot}%{_unitdir}
install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 root root -
EOF

%else
install -d %{buildroot}%{_sysconfdir}/init.d
install -m 755 %{SOURCE2}  %{buildroot}%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
%endif

%pre
groupadd -r repmgr >/dev/null 2>&1 || :
useradd -m -g repmgr -r -s /bin/bash \
        -c "repmgr" repmgr >/dev/null 2>&1 || :
if [ ! -x /var/log/repmgr ]
then
	%{__mkdir} -m 700 /var/log/repmgr
	chown repmgr: /var/log/repmgr
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
%{__chown} repmgr: %{_localstatedir}/run/%{sname}

%postun -p /sbin/ldconfig

%files
%doc CREDITS HISTORY LICENSE README.rst TODO COPYRIGHT
%dir %{pginstdir}/bin
%dir %{_sysconfdir}/%{sname}/%{pgpackageversion}/
%config %{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf
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
%{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/%{sname}-%{pgpackageversion}
%endif

%changelog
* Fri May 1 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-4
- chown pid file dir and fix its path.
- Fix unit file
- Remove license macro in RHEL 6 spec.

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
