%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global pgpoolinstdir /usr/pgpool-9.1
%global sname pgpool-II
%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%global _varrundir %{_localstatedir}/run/%{name}

Summary:		Pgpool is a connection pooling/replication server for PostgreSQL
Name:			%{sname}-%{pgmajorversion}
Version:		3.5.4
Release:		1%{?dist}
License:		BSD
Group:			Applications/Databases
URL:			http://pgpool.net
Source0:		http://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Source1:		%{sname}-%{pgmajorversion}.service
Source2:		pgpool.sysconfig
Source3:		pgpool.init
Source9:		pgpool-%{pgmajorversion}-libs.conf
Patch1:			pgpool.conf.sample.patch
Patch2:			pgpool-Makefiles-pgxs.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:		postgresql%{pgmajorversion}-devel pam-devel, libmemcached-devel
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
Obsoletes:		postgresql-pgpool > 1.0.0

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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for pgpool-II.

%package extensions
Summary:	Postgersql extensions for pgpool-II
Group:		Applications/Databases
Obsoletes:	postgresql-pgpool-II-recovery <= 1:3.3.4-1
Provides:	postgresql-pgpool-II-recovery = %{version}-%{release}
Requires:	postgresql%{pgmajorversion}-server

%description extensions
Postgresql extensions libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0
%patch2 -p0

%build
./configure \
	--datadir=%{pgpoolinstdir}/share \
	--disable-static \
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

USE_PGXS=1 make %{?_smp_mflags}
USE_PGXS=1 make %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 make %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 make %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
make %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
make %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 root root -
EOF

%else
%{__install} -d %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif

%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %{buildroot}%{pgpoolinstdir}/share/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{pgpoolinstdir}/share/

%post
# Create alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_pool_status pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_promote_node pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pcp_watchdog pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/pgpool-libs.conf pgpool-ld-conf %{pgpoolinstdir}/share/pgpool-%{pgmajorversion}-libs.conf %{pgmajorversion}0
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%tmpfiles_create
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}
%endif

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
	%{_sbindir}/update-alternatives --remove pgpool-ld-conf	%{pgpoolinstdir}/share/pgpool-%{pgmajorversion}-libs.conf
	/sbin/ldconfig
fi
/sbin/ldconfig
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
	%{_sbindir}/update-alternatives --remove pgpool-pgpool %{pgpoolinstdir}/bin/pgpool
	%{_sbindir}/update-alternatives --remove pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count
	%{_sbindir}/update-alternatives --remove pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info
	%{_sbindir}/update-alternatives --remove pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status
	%{_sbindir}/update-alternatives --remove pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count
	%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info
	%{_sbindir}/update-alternatives --remove pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool
	%{_sbindir}/update-alternatives --remove pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node
	%{_sbindir}/update-alternatives --remove pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info
	%{_sbindir}/update-alternatives --remove pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5
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
%doc README TODO INSTALL AUTHORS ChangeLog NEWS doc/pgpool-en.html doc/pgpool-ja.html doc/pgpool.css doc/tutorial-en.html doc/tutorial-ja.html
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%dir %{pgpoolinstdir}
%{pgpoolinstdir}/bin/pgpool
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
%{pgpoolinstdir}/man/man8/pgpool.8
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{_sysconfdir}/%{name}/*.sample*
%{pgpoolinstdir}/lib/libpcp.so.*
%config(noreplace) %attr (644,root,root) %{pgpoolinstdir}/share/pgpool-%{pgmajorversion}-libs.conf
%if %{systemd_enabled}
%ghost %{_varrundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%else
%{_sysconfdir}/init.d/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

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
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_recovery--1.1.sql
%{pginstdir}/share/extension/pgpool_recovery.control
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
# From PostgreSQL 9.4 pgpool-regclass.so is not needed anymore
# because 9.4 or later has to_regclass.
%{pginstdir}/lib/pgpool-regclass.so

%changelog
* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.4-1
- Update to 3.5.4

* Mon Jul 4 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-1
- Update to 3.5.3

* Thu Apr 28 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-1
- Update to 3.5.2

* Tue Apr 5 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.1-1
- Update to 3.5.1

* Tue Feb 9 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0
- Add pgpool_adm to extensions subpackage.

* Mon Jan 11 2016 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-4
- Second time in a row: Fix typo in init script. Per report
  from Ryan Shoemaker.

* Wed Dec 9 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-3
- Fix typo in init script. Per report from Ryan Shoemaker.

* Thu Sep 17 2015 Jeff Frost <jeff@pgexperts.com> - 3.4.3-2
- Bring init script in line with pgpool community init script

* Wed Aug 5 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-1
- Update to 3.4.3, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.4.3/NEWS.txt

* Wed Apr 8 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.2-1
- Update to 3.4.2, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.4.2/NEWS.txt

* Fri Feb 6 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-2
- Add missing BuildRoot macro.
- Fix rpmlint warnings/errors.

* Thu Feb 5 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1
- Remove patch3, now in upstream.

* Mon Jan 12 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-4
- Create /etc/ld.so.conf.d config file, for pcp and other libraries.
  Per #12597 in pgsql-bugs mailing list.

* Mon Jan 12 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-3
- Fix builds for non-systemd environments. Patch by Bernd Helmle.

* Thu Dec 11 2014 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-2
- Sync with Fedora spec and apply our multiversion changes.
  Fedora spec is recently reworked by Pavel Raiskup. This spec
  file adds -extensions subpackage.

- Trim changelog

* Fri Nov 7 2014 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0
- Add patch3 to fix compilation with memcache support. This
  patch will be removed when 3.4.1 comes out.
- Fix config file path in unit file.

