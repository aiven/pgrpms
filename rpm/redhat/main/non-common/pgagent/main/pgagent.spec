%global _vpath_builddir .
%global sname	pgagent

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.2.2
Release:	3%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgadmin-org/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz
Source2:	%{sname}-%{pgmajorversion}.service
URL:		https://github.com/pgadmin-org/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 3.0.0
%endif

BuildRequires:	boost-devel >= 1.41

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
%setup -q -n %{sname}-%{sname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie -pthread -std=c++11"
export CFLAGS
export CXXFLAGS

%cmake3	\
	-D CMAKE_INSTALL_PREFIX:PATH=/usr \
	-D PG_CONFIG_PATH:FILEPATH=%{pginstdir}/bin/pg_config \
	-D STATIC_BUILD:BOOL=OFF .

%install
%{__rm} -rf %{buildroot}
%{__make} -C "%{_vpath_builddir}" DESTDIR=%{buildroot} install

# Rename pgagent binary, so that we can have parallel installations:
%{__mv} -f %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}
# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}_%{pgmajorversion}.service
# Install conf file
%{__install} -p -d %{buildroot}%{_sysconfdir}/%{sname}/
cat > %{buildroot}%{_sysconfdir}/%{sname}/%{name}.conf <<EOF
DBNAME=postgres
DBUSER=postgres
DBHOST=127.0.0.1
DBPORT=5432
LOGFILE=/var/log/pgagent_%{pgmajorversion}.log
EOF
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 root root -
EOF

# Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} <<EOF
/var/log/pgagent_%{pgmajorversion}.log {
    missingok
    compress
    notifempty
    sharedscripts
    create 0640 pgagent pgagent
    nodateext
    weekly
    rotate 5
}
EOF

%post
if [ $1 -eq 1 ] ; then
%systemd_post %{sname}_%{pgmajorversion}.service
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}_%{pgmajorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}_%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

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
%doc README
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%ghost %{_rundir}/%{sname}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}_%{pgmajorversion}.service
%dir %{_sysconfdir}/%{sname}/
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{sname}/%{name}.conf
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sat Feb 4 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-3
- Switch on C++11 support on older GCC versions (in this case,
  RHEL 7).

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Sep 14 2022 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1
- Update to 4.2.2
- Update URLs

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1
- Move .conf and .logrotate files to spec file, so that we
  do less work during each PostgreSQL major release.

* Thu Apr 1 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-0
- Update to 4.2.1

* Thu Oct 29 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-5
- Use cmake3 macro to build packages, and define vpath_builddir macro
  manually. This will solve the FTBFS issue on Fedora 33, per:
  https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
  Also works on the other distros.

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

