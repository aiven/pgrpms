%global sname	pgagent

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.0.0
Release:	4%{?dist}
License:	PostgreSQL
Source0:	https://download.postgresql.org/pub/pgadmin/%{sname}/pgAgent-%{version}-Source.tar.gz
Source2:	%{sname}-%{pgmajorversion}.service
Source3:	%{sname}-%{pgmajorversion}.init
Source4:	%{sname}-%{pgmajorversion}.logrotate
Source5:	%{sname}-%{pgmajorversion}.conf
URL:		http://www.pgadmin.org/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 2.8.8
%endif

BuildRequires:	boost-devel >= 1.41

%if %{systemd_enabled}
BuildRequires:		systemd, systemd-devel
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

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgAgent is a job scheduler for PostgreSQL which may be managed
using pgAdmin.

%pre
if [ $1 -eq 1 ] ; then
groupadd -r pgagent >/dev/null 2>&1 || :
useradd -g pgagent -r -s /bin/false \
	-c "pgAgent Job Scheduler" pgagent >/dev/null 2>&1 || :
touch /var/log/pgagent_%{pgmajorversion}.log
fi
%{__chown} pgagent:pgagent /var/log/pgagent_%{pgmajorversion}.log
%{__chmod} 0700 /var/log/pgagent_%{pgmajorversion}.log

%prep
%setup -q -n pgAgent-%{version}-Source

%build
%ifarch ppc64 ppc64le
	CFLAGS="-O3 -mcpu=power8 -mtune=power8"; export CFLAGS
	CC=%{atpath}/bin/gcc; export CC
	LDFLAGS="-pthread"; export LDFLAGS
	BOOST_INCLUDEDIR=%{atpath}/include; export BOOST_INCLUDEDIR
	BOOST_LIBRARYDIR=%{atpath}/lib64; export BOOST_LIBRARYDIR
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie -pthread"
	export CFLAGS
	export CXXFLAGS
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
cmake3 .. \
%else
%cmake .. \
%endif
	-D CMAKE_INSTALL_PREFIX:PATH=/usr \
	-D PG_CONFIG_PATH:FILEPATH=/%{pginstdir}/bin/pg_config \
	-D STATIC_BUILD:BOOL=OFF .

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

# Rename pgagent binary, so that we can have parallel installations:
%{__mv} -f %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}
# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

%if %{systemd_enabled}
# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}_%{pgmajorversion}.service
# Install conf file
%{__install} -p -d %{buildroot}%{_sysconfdir}/%{sname}/
%{__install} -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{sname}/%{name}.conf
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 root root -
EOF
%else
# install init script
%{__install} -d %{buildroot}%{_initrddir}
%{__install} -m 755 %{SOURCE3} %{buildroot}/%{_initrddir}/%{name}
%endif

# Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%post
if [ $1 -eq 1 ] ; then
%if %{systemd_enabled}
%systemd_post %{sname}_%{pgmajorversion}.service
%else
chkconfig --add %{name}
%endif
fi

%preun
%if %{systemd_enabled}
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}_%{pgmajorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}_%{pgmajorversion}.service >/dev/null 2>&1 || :
fi
%else
	chkconfig --del %{name}
%endif

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{sname}_%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if %{systemd_enabled}
%doc README
%license LICENSE
%else
%doc README LICENSE
%endif
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%if %{systemd_enabled}
%ghost %{_rundir}/%{sname}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}_%{pgmajorversion}.service
%dir %{_sysconfdir}/%{sname}/
%config(noreplace) %{_sysconfdir}/%{sname}/%{name}.conf
%else
%{_initrddir}/%{name}
%endif
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Mar 23 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-4
- Make sure that pgAgent restarts itself after a failure.

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-3.1
- Rebuild for PostgreSQL 12

* Fri Apr 12 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-3
- Really fix pgAgent tmpfiles.d directory.

* Fri Jan 4 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-2
- Fix/update pgAgent tmpfiles.d directory.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 9 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0
- Add -pthread to CXXFLAGS

* Tue Oct 17 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-10
- Move configuration parameters out of the unit file to a
  new config file.
- Add a new patch to fix builds against PostgreSQL 10

* Sun Jul 30 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-9
- Install a logrotate file.

* Fri Jul 28 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-8
- Improve unit file, so that pgagent actually stops.

* Mon Jul 24 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-7
- Fix unit file name in spec file, per Fahar Abbas (EDB QA testing)

* Tue Jul 18 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-6
- Add wxBase dependency, per Fahar Abbas (EDB QA testing)

* Fri Nov 11 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-5
- Install init script on RHEL <= 6, not unit file.

* Wed Oct 19 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-4
- Fix PostgreSQL version in unit file and init script. Per
  report from Alf Normann Klausen, pgsql bug #14370.

* Fri Jan 22 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-3
- Create unified spec file that works with all distros.
- Fix an issue with user and group creation.

* Wed Dec 30 2015 Devrim Gündüz <devrim@gunduz.org> 3.4.0-2
- Build with -fPIC, per Fedora 23+ guidelines.
- Use more macros.
- Update license.
- Update download URL.

* Fri Oct 17 2014 Devrim Gündüz <devrim@gunduz.org> 3.4.0-1
- Update to 3.4.0
- Use macros for pgagent, where appropriate.
- Switch to systemd, and use unit file instead of sysV init
  script.
- Add PostgreSQL major version number to pgagent binary, to
  enable parallel installations.

* Mon Sep 17 2012 Devrim Gündüz <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Wed Sep 12 2012 Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Various updates from David Wheeler
- Update to 3.2.1
- Improve init script

* Tue Dec 6 2011 Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Initial packaging

