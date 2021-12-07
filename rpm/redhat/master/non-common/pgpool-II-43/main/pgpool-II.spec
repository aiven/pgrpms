%global pgpoolinstdir /usr/pgpool-II-%{pgpackageversion}
%global sname pgpool-II

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

%ifarch ppc64 ppc64le
%global llvm	0
%else
%global llvm	1
%endif

Summary:		Pgpool is a connection pooling/replication server for PostgreSQL
Name:			%{sname}-%{pgmajorversion}
Version:		4.3.0
Release:		1%{?dist}
License:		BSD
URL:			http://pgpool.net
Source0:		http://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Source1:		%{sname}-pg%{pgmajorversion}.service
Source2:		%{sname}.sysconfig
Patch1:			%{sname}-pg%{pgmajorversion}-conf.sample.patch

BuildRequires:		postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:		libmemcached-devel openssl-devel pgdg-srpm-macros

Requires:		libmemcached
Requires(pre):		/usr/sbin/useradd /usr/sbin/groupadd

BuildRequires:		systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version} && 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%else
Requires(post):		systemd-sysv
%endif
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

# The path to the config files is different in older
# versions of pgpool.  Let's conflict so that an upgrade
# would need to be a manual process to be safe.
Conflicts:	%{sname}_%{pgmajorversion}

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

%description devel
Development headers and libraries for pgpool-II.

%package extensions
Summary:	Postgresql extensions for pgpool-II
Obsoletes:	postgresql-pgpool-II-recovery <= 1:3.3.4-1
Provides:	postgresql-pgpool-II-recovery = %{version}-%{release}
Requires:	postgresql%{pgmajorversion}-server

%description extensions
Postgresql extensions libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

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

export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
export PATH=%{pginstdir}/bin/:$PATH
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{name} 0755 postgres postgres -
EOF

# Create the directory for the pid files (defined in pgpool.conf.sample)
%{__install} -d -m 755 %{buildroot}/run/%{name}

%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

# Create linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{geosinstdir}/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{sname}-pgdg-libs.conf

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

/sbin/ldconfig
%systemd_post %{sname}-%{pgmajorversion}.service

# Create log directory
%{__mkdir} -p /var/log/%{name}
%{__chown} postgres: /var/log/%{name}

%preun
%systemd_preun %{sname}-%{pgmajorversion}.service

%postun
if [ "$1" -eq 0 ]
  then
	/sbin/ldconfig
fi
/sbin/ldconfig
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%endif
%endif

%systemd_postun_with_restart %{sname}-%{pgmajorversion}.service

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

%triggerun -- %{sname}-%{pgmajorversion} < 3.1-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pgpool
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save %{sname}-%{pgmajorversion} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{sname}-%{pgmajorversion} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :

%files
%doc README TODO INSTALL AUTHORS ChangeLog NEWS
%license COPYING
%dir %{pgpoolinstdir}
%{pgpoolinstdir}/bin/pgpool
%{pgpoolinstdir}/bin/pg_enc
%{pgpoolinstdir}/bin/pgproto
%{pgpoolinstdir}/bin/pcp_attach_node
%{pgpoolinstdir}/bin/pcp_detach_node
%{pgpoolinstdir}/bin/pcp_health_check_stats
%{pgpoolinstdir}/bin/pcp_node_count
%{pgpoolinstdir}/bin/pcp_node_info
%{pgpoolinstdir}/bin/pcp_pool_status
%{pgpoolinstdir}/bin/pcp_proc_count
%{pgpoolinstdir}/bin/pcp_proc_info
%{pgpoolinstdir}/bin/pcp_promote_node
%{pgpoolinstdir}/bin/pcp_recovery_node
%{pgpoolinstdir}/bin/pcp_reload_config
%{pgpoolinstdir}/bin/pcp_stop_pgpool
%{pgpoolinstdir}/bin/pcp_watchdog_info
%{pgpoolinstdir}/bin/pg_md5
%{pgpoolinstdir}/bin/pgpool_setup
%{pgpoolinstdir}/bin/watchdog_setup
%{pgpoolinstdir}/bin/wd_cli
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{_sysconfdir}/%{name}/*.sample*
%{pgpoolinstdir}/lib/libpcp.so*
%{_sysconfdir}/ld.so.conf.d/%{sname}-pgdg-libs.conf

%ghost %{_rundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %if %llvm
 %{pginstdir}/lib/bitcode/pgpool*.bc
 %{pginstdir}/lib/bitcode/pgpool_adm/*.bc
 %{pginstdir}/lib/bitcode/pgpool-regclass/*.bc
 %{pginstdir}/lib/bitcode/pgpool-recovery/*.bc
 %endif
 %endif
%endif
%attr(755,postgres,postgres) %dir /run/%{name}

%files devel
%{pgpoolinstdir}/include/libpcp_ext.h
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_process_reporting.h
%{pgpoolinstdir}/include/pool_type.h

%files extensions
%{pginstdir}/lib/pgpool_adm.so
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/share/extension/pgpool_adm*.sql
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool_recovery*.sql
%{pginstdir}/share/extension/pgpool_recovery.control
# From PostgreSQL 9.4 pgpool-regclass.so is not needed anymore
# because 9.4 or later has to_regclass.
%{pginstdir}/lib/pgpool-regclass.so

%changelog
* Tue Dec 7 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Initial packaging for 4.3 series.

