%global pgpoolinstdir /usr/pgpool-%{pgpackageversion}
%global sname pgpool-II

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

# Use this macro for update-alternatives, because implementations are different
# between RHEL and SLES:
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
%global __update_alternatives %{_sbindir}/update-alternatives --quiet
%endif
%else
%global __update_alternatives %{_sbindir}/update-alternatives
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:		Pgpool is a connection pooling/replication server for PostgreSQL
Name:			%{sname}_%{pgmajorversion}
Version:		4.0.16
Release:		1%{?dist}
License:		BSD
URL:			http://pgpool.net
Source0:		http://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Source1:		%{sname}-pg%{pgmajorversion}.service
Source2:		%{sname}.sysconfig
%if ! %{systemd_enabled}
Source3:		%{sname}-pg%{pgmajorversion}.init
%endif
Source9:		%{sname}-pg%{pgmajorversion}-libs.conf
Patch1:			%{sname}-pg%{pgmajorversion}-conf.sample.patch
Patch2:			%{sname}-pg%{pgmajorversion}-makefiles-pgxs.patch

BuildRequires:		postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:		libmemcached-devel openssl-devel pgdg-srpm-macros

Requires:		libmemcached
Requires(pre):		/usr/sbin/useradd /usr/sbin/groupadd

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

Obsoletes:		postgresql-pgpool < 1.0.0
Obsoletes:		%{sname}-%{pgmajorversion} < 4.0.11-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgpool-II is a inherited project of pgpool (to classify from
pgpool-II, it is sometimes called as pgpool-I). For those of
you not familiar with pgpool-I, it is a multi-functional
middle ware for PostgreSQL that features connection pooling,
replication and load balancing functions. pgpool-I allows a
user to connect at most two PostgreSQL servers for higher
availability or for higher search performance compared to a
single PostgreSQL server.

pgpool-II, on the other hand, allows multiple PostgreSQL
servers (DB nodes) to be connected, which enables queries
to be executed simultaneously on all servers. In other words,
it enables "parallel query" processing. Also, pgpool-II can
be started as pgpool-I by changing configuration parameters.
pgpool-II that is executed in pgpool-I mode enables multiple
DB nodes to be connected, which was not possible in pgpool-I.

%package devel
Summary:	The development files for pgpool-II
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{sname}-%{pgmajorversion}-devel < 4.0.11-2

%description devel
Development headers and libraries for pgpool-II.

%package extensions
Summary:	Postgresql extensions for pgpool-II
Obsoletes:	postgresql-pgpool-II-recovery <= 1:3.3.4-1
Provides:	postgresql-pgpool-II-recovery = %{version}-%{release}
Requires:	postgresql%{pgmajorversion}-server
Obsoletes:	%{sname}-%{pgmajorversion}-extensions < 4.0.11-2

%description extensions
Postgresql extensions libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0
%patch2 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

# We need this flag on SLES so that pgpool can find libmemched.
# Otherwise, we get "libmemcached.so: undefined reference to `pthread_once'" error.
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
	export LDFLAGS='-lpthread'
%endif
%endif
%ifarch ppc64 ppc64le
%configure --build=ppc64le \
%else
./configure \
%endif
	--datadir=%{pgpoolinstdir}/share \
	--disable-static \
	--bindir=%{pgpoolinstdir}/bin \
	--exec-prefix=%{pgpoolinstdir} \
	--includedir=%{pgpoolinstdir}/include \
	--libdir=%{pgpoolinstdir}/lib \
	--mandir=%{pgpoolinstdir}/man \
	--sysconfdir=%{_sysconfdir}/%{name}/ \
	--with-memcached=%{_includedir}/libmemcached \
	--with-openssl \
	--with-pam \
	--with-pgsql=%{pginstdir}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{name} 0755 postgres postgres -
EOF

%else
%{__install} -d %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif

# Create the directory for the pid files (defined in pgpool.conf.sample)
%{__install} -d -m 755 %{buildroot}/var/run/%{name}

%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %{buildroot}%{pgpoolinstdir}/share/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{pgpoolinstdir}/share/

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
# Create alternatives entries for common binaries and man files
%{__update_alternatives} --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_pool_status pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_promote_node pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_watchdog_info pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 %{pgmajorversion}0
%{__update_alternatives} --install /etc/ld.so.conf.d/pgpool-libs.conf pgpool-ld-conf %{pgpoolinstdir}/share/pgpool-II-pg%{pgmajorversion}-libs.conf %{pgmajorversion}0

/sbin/ldconfig
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}
%endif
# Create log directory
%{__mkdir} -p /var/log/%{name}
%{__chown} postgres: /var/log/%{name}

%preun
%if %{systemd_enabled}
%systemd_preun %{sname}-%{pgmajorversion}.service
%else
if [ $1 -eq 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	/sbin/chkconfig --del %{sname}-%{pgmajorversion}
fi
%endif

%postun
if [ "$1" -eq 0 ]
  then
	%{__update_alternatives} --remove pgpool-ld-conf	%{pgpoolinstdir}/share/pgpool-II-pg%{pgmajorversion}-libs.conf
	/sbin/ldconfig
fi
/sbin/ldconfig
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%endif
%endif

%if %{systemd_enabled}
%systemd_postun_with_restart %{sname}-%{pgmajorversion}.service
%else
if [ $1 -ge 1 ] ; then
    /sbin/service pgpool-II-%{pgmajorversion} condrestart >/dev/null 2>&1 || :
fi
%endif
# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{__update_alternatives} --remove pgpool-pgpool %{pgpoolinstdir}/bin/pgpool
	%{__update_alternatives} --remove pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node
	%{__update_alternatives} --remove pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node
	%{__update_alternatives} --remove pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count
	%{__update_alternatives} --remove pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info
	%{__update_alternatives} --remove pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status
	%{__update_alternatives} --remove pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node
	%{__update_alternatives} --remove pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count
	%{__update_alternatives} --remove pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info
	%{__update_alternatives} --remove pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool
	%{__update_alternatives} --remove pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node
	%{__update_alternatives} --remove pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info
	%{__update_alternatives} --remove pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5
fi

%if %{systemd_enabled}
%triggerun -- %{sname}-%{pgmajorversion} < 3.1-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pgpool
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save %{sname}-%{pgmajorversion} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{sname}-%{pgmajorversion} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
%endif

%files
%doc README TODO INSTALL AUTHORS ChangeLog NEWS
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%dir %{pgpoolinstdir}
%{pgpoolinstdir}/bin/pgpool
%{pgpoolinstdir}/bin/pg_enc
%{pgpoolinstdir}/bin/pgproto
%{pgpoolinstdir}/bin/pcp_attach_node
%{pgpoolinstdir}/bin/pcp_detach_node
%{pgpoolinstdir}/bin/pcp_node_count
%{pgpoolinstdir}/bin/pcp_node_info
%{pgpoolinstdir}/bin/pcp_pool_status
%{pgpoolinstdir}/bin/pcp_proc_count
%{pgpoolinstdir}/bin/pcp_proc_info
%{pgpoolinstdir}/bin/pcp_promote_node
%{pgpoolinstdir}/bin/pcp_recovery_node
%{pgpoolinstdir}/bin/pcp_stop_pgpool
%{pgpoolinstdir}/bin/pcp_watchdog_info
%{pgpoolinstdir}/bin/pg_md5
%{pgpoolinstdir}/bin/pgpool_setup
%{pgpoolinstdir}/bin/watchdog_setup
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{_sysconfdir}/%{name}/*.sample*
%{pgpoolinstdir}/lib/libpcp.so.*
%config(noreplace) %attr (644,root,root) %{pgpoolinstdir}/share/pgpool-II-pg%{pgmajorversion}-libs.conf

%if %{systemd_enabled}
%ghost %{_rundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%else
%{_sysconfdir}/init.d/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %{pginstdir}/lib/bitcode/pgpool*.bc
 %{pginstdir}/lib/bitcode/pgpool_adm/*.bc
 %{pginstdir}/lib/bitcode/pgpool-regclass/*.bc
 %{pginstdir}/lib/bitcode/pgpool-recovery/*.bc
 %endif
%endif
%attr(755,postgres,postgres) %dir /var/run/%{name}

%files devel
%{pgpoolinstdir}/include/libpcp_ext.h
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_process_reporting.h
%{pgpoolinstdir}/include/pool_type.h
%{pgpoolinstdir}/lib/libpcp.so

%files extensions
%{pginstdir}/lib/pgpool_adm.so
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/share/extension/pgpool_adm--1.0.sql
%{pginstdir}/share/extension/pgpool_adm--1.0--1.1.sql
%{pginstdir}/share/extension/pgpool_adm--1.1.sql
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool_recovery--1.1.sql
%{pginstdir}/share/extension/pgpool_recovery.control
%{pginstdir}/share/extension/pgpool_recovery--1.1--1.2.sql
%{pginstdir}/share/extension/pgpool_recovery--1.2.sql
# From PostgreSQL 9.4 pgpool-regclass.so is not needed anymore
# because 9.4 or later has to_regclass.
%{pginstdir}/lib/pgpool-regclass.so

%changelog
* Mon Nov 22 2021 - John Harvey <john.harvey@crunchydata.com> 4.0.16-1
- Update to 4.0.16. Fix sample file pathing issue.

* Wed Nov 25 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.12-2
- Also obsolete subpackages.

* Tue Nov 24 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.12-1
- Update to 4.0.12

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.11-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 17 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.11-1
- Update to 4.0.11

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.10-1
- Update to 4.0.10

* Thu May 21 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.9-1
- Update to 4.0.9

* Wed Feb 26 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.8-1
- Update to 4.0.8

* Fri Dec 20 2019 - John Harvey <john.harvey@crunchydata.com> 4.0.7-2
- Make sure that directory /var/run/pgpool-II is created with the RPM.
  This will ensure that pgpool.conf.sample will work with its defaults.

* Fri Nov 1 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.7-1
- Update to 4.0.7
- Fix F-31 packaging by removing unused macro in the spec file.

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.6-1.1
- Rebuild for PostgreSQL 12

* Thu Aug 15 2019 Devrim Gündüz <devrim@gunduz.org> 4.0.6-1
- Update to 4.0.6

* Thu May 16 2019 Devrim Gündüz <devrim@gunduz.org> 4.0.5-1
- Update to 4.0.5

* Thu Mar 7 2019 John K. Harvey <john.harvey@crunchydata.com> - 4.0.3-3
- Fix typo in -extensions package

* Tue Mar 5 2019 Devrim Gündüz <devrim@gunduz.org> 4.0.3-2
- Fix pcp_watchdog_info alternatives link, per Matthias Steppuhn.

* Thu Feb 21 2019 Devrim Gündüz <devrim@gunduz.org> 4.0.3-1
- Update to 4.0.3

* Mon Jan 21 2019 Devrim Gündüz <devrim@gunduz.org> 4.0.2-4
- Add Reload target to unit file

* Sun Dec 23 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.2-3
- Fix tmpfiles.d file

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.2-2
- Run pgpool with postgres user
- Create pgPool log directory
- Fix tmpfiles path
- Add -D to sysconfig file.

* Fri Nov 30 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.2-1
- Update to 4.0.2

* Wed Oct 31 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1

* Fri Oct 19 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 3.7.5-2
- Rebuild against PostgreSQL 11.0

* Wed Aug 1 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.5-1
- Update to 3.7.5

* Tue Jul 17 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.4-2
- Add PostgreSQL 11 support.

* Thu Jun 14 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.4-1
- Update to 3.7.4

* Tue Apr 17 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.3-1
- Update to 3.7.3

* Sat Feb 17 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.2-1
- Update to 3.7.2

* Wed Jan 10 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.1-1
- Update to 3.7.1

* Sun Nov 26 2017 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-1
- Initial packaging for 3.7.0

