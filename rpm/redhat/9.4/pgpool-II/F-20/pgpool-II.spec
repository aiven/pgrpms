%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global pgpoolinstdir /usr/pgpool-9.4
%global sname pgpool-II

%if 0%{?rhel} && 0%{?rhel} <= 6
%define systemd_enabled 0
%else
%define systemd_enabled 1
%endif

%global _varrundir %{_localstatedir}/run/pgpool


Summary:	Pgpool is a connection pooling/replication server for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	3.3.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://www.pgpool.net
Source0:	http://www.pgpool.net/download.php?f=%{sname}-%{version}.tar.gz
Source1:        pgpool.init
Source2:        pgpool.sysconfig
Source3:	pgpool-II-94.service
Patch1:		pgpool.conf.sample.patch
Patch2:		pgpool-Makefiles-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, pam-devel, libmemcached-devel
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
Requires(post):		%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Obsoletes:	postgresql-pgpool

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
Summary:	The  development files for pgpool-II
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development headers and libraries for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0
%patch2 -p0

%build
./configure --exec-prefix=%{pgpoolinstdir} --with-pgsql=%{pginstdir} \
--disable-static --with-pam --disable-rpath --sysconfdir=%{_sysconfdir}/%{name}/ \
--includedir=%{pgpoolinstdir}/include --datadir=%{pgpoolinstdir}/share \
--mandir=%{pgpoolinstdir}/man --with-openssl --with-memcached=%{_includedir}/libmemcached

USE_PGXS=1 make %{?_smp_flags}
USE_PGXS=1 make -C sql %{?_smp_flags}

%install
rm -rf %{buildroot}
make %{?_smp_flags} DESTDIR=%{buildroot} install
make -C sql %{?_smp_flags} DESTDIR=%{buildroot} install


%if %{systemd_enabled}
install -d %{buildroot}%{_unitdir}
install -m 755 %{SOURCE3} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service
# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 root root -
EOF
%else
# Install init script,, and sysconfig file:
install -d %{buildroot}%{_initrddir}
sed 's/^PGVERSION=.*$/PGVERSION=%{pgmajorversion}/' <%{SOURCE1} > pgpool-II-%{pgmajorversion}.init
install -m 755 pgpool-II-%{pgmajorversion}.init %{buildroot}%{_initrddir}/pgpool-II-%{pgmajorversion}
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/pgpool-II-%{pgmajorversion}
%endif

# nuke libtool archive and static lib
rm -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

%clean
rm -rf %{buildroot}

%post
# Create alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_pool_status pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_promote_node pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node 930
%{_sbindir}/update-alternatives --install /usr/bin/pcp_systemdb_info pgpool-pcp_systemdb_info %{pgpoolinstdir}/bin/cp_systemdb_info 930
%{_sbindir}/update-alternatives --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 930
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add pgpool
%endif
%tmpfiles_create

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
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_postun_with_restart %{sname}-%{pgmajorversion}.service
%else
if [ $1 -ge 1 ] ; then
# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]
  then
      	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgpool-pgpool %{pgpoolinstdir}/bin/pgpool
	%{_sbindir}/update-alternatives --remove pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count
	%{_sbindir}/update-alternatives --remove pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info
	%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count
	%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info
	%{_sbindir}/update-alternatives --remove pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool
	%{_sbindir}/update-alternatives --remove pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_systemdb_info %{pgpoolinstdir}/bin/cp_systemdb_info
	%{_sbindir}/update-alternatives --remove pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5
fi
    /sbin/service pgpool condrestart >/dev/null 2>&1 || :fi
%endif

%if %{systemd_enabled}
%triggerun -- pgpool < 3.1-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pgpool
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save pgpool >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del pgpool >/dev/null 2>&1 || :
/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
%endif


%files
%defattr(-,root,root,-)
#%dir %{_datadir}/%{name}
%{pgpoolinstdir}/bin/pgpool
%{pgpoolinstdir}/bin/pcp_attach_node
%{pgpoolinstdir}/bin/pcp_detach_node
%{pgpoolinstdir}/bin/pcp_node_count
%{pgpoolinstdir}/bin/pcp_node_info
%{pgpoolinstdir}/bin/pcp_pool_status
%{pgpoolinstdir}/bin/pcp_promote_node
%{pgpoolinstdir}/bin/pcp_proc_count
%{pgpoolinstdir}/bin/pcp_proc_info
%{pgpoolinstdir}/bin/pcp_stop_pgpool
%{pgpoolinstdir}/bin/pcp_recovery_node
%{pgpoolinstdir}/bin/pcp_systemdb_info
%{pgpoolinstdir}/bin/pcp_watchdog_info
%{pgpoolinstdir}/bin/pg_md5
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pcp.conf.sample
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-master-slave
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-replication
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-stream
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pool_hba.conf.sample
%{pgpoolinstdir}/lib/libpcp.so*
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/lib/pgpool-regclass.so
%{pgpoolinstdir}/man/man8/pgpool.8
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{pgpoolinstdir}/share/pgpool-II/system_db.sql
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_recovery*
%{pginstdir}/share/extension/pgpool_regclass*
%if %{systemd_enabled}
%ghost %{_varrundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%else
%{_initrddir}/%{sname}-%{pgmajorversion}
%{_sysconfdir}/sysconfig/%{sname}-%{pgmajorversion}
%endif


%files devel
%defattr(-,root,root,-)
%{pgpoolinstdir}/include/libpcp_ext.h
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_type.h
%{pgpoolinstdir}/include/pool_process_reporting.h

%changelog
* Fri Jun 20 2014 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.3-1
- Update to 3.3.3
- Apply various parts from Fedora spec file.

* Thu Feb 20 2014 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.2-1
- Update to 3.3.2

* Tue Nov 12 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1
- Add pgpool-recovery and pgpool-regclass extensions. Per 
  pgrpms #127 and #134 .
- Compile pgpool with memcache support, per pgrpms #135.

* Fri Aug 16 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0
- Compile pgpool with OpenSSL support, per #44
- Trim changelog

* Wed Sep 12 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Tue Jul 03 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.1.3-2
- Update download URL.

* Tue Apr 24 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.1.3/doc/NEWS.txt
- Update patch1
- Update alternatives version to 930

* Tue Mar 27 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.1.2-1
- Update to 3.1.2, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.1.2/doc/NEWS.txt

* Fri Aug 12 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.4
- Update to 3.0.4

* Tue Nov 9 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.1
- Update to 3.0.1
- Apply many 9.0+ specific changes, and use alternatives method.
- Apply some changes to init script.

* Sun Sep 26 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.0
- Update to 3.0

* Thu Jul 1 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.3.3-1
- Update to 2.3.3
- Enable compilation with PostgreSQL 9.0.

* Thu Dec 10 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Tue Dec 1 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.6-1
- Update to 2.2.6

* Sun Nov 01 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.5-2
- Remove init script from all runlevels before uninstall. Per #RH Bugzilla
  532177

* Sun Oct 4 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5, for various fixes described at
  http://lists.pgfoundry.org/pipermail/pgpool-general/2009-October/002188.html
- Re-apply a fix for Red Hat Bugzilla #442372

* Wed Sep 9 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Wed May 6 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sun Mar 1 2009 Devrim Gunduz <devrim@gunduz.org> 2.2-1
- Update to 2.2
- Fix URL
- Own /usr/share/pgpool-II directory.
- Fix pid file path in init script, per	pgcore #81.
- Fix spec file -- we don't use short_name macro in pgcore spec file.
- Create pgpool pid file directory, per pgcore #81.
- Fix stop/start routines, also improve init script a bit.
- Install conf files to a new directory (/etc/pgpool-II), and get rid 
  of sample conf files.

* Fri Aug 8 2008 Devrim Gunduz <devrim@gunduz.org> 2.1-1
- Update to 2.1
- Removed temp patch #4.

* Sun Jan 13 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Add a temp patch that will disappear in 2.0.2

