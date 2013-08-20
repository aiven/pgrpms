%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global pgpoolinstdir /usr/pgpool-9.2
%global sname pgpool-II

Summary:	Pgpool is a connection pooling/replication server for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	3.3.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://www.pgpool.net
Source0:	http://www.pgpool.net/download.php?f=%{sname}-%{version}.tar.gz
Source1:        pgpool.init
Source2:        pgpool.sysconfig
Patch1:		pgpool.conf.sample.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel pam-devel
Requires(post):	%{_sbindir}/update-alternatives
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

%build
./configure --exec-prefix=%{pgpoolinstdir} --with-pgsql=%{pginstdir} \
--disable-static --with-pam --disable-rpath --sysconfdir=%{_sysconfdir}/%{name}/ \
--includedir=%{pgpoolinstdir}/include --datadir=%{pgpoolinstdir}/share \
--mandir=%{pgpoolinstdir}/man --with-openssl

make %{?_smp_flags}

%install
rm -rf %{buildroot}
make %{?_smp_flags} DESTDIR=%{buildroot} install
install -d %{buildroot}%{_initrddir}
sed 's/^PGVERSION=.*$/PGVERSION=%{pgmajorversion}/' <%{SOURCE1} > pgpool-II-%{pgmajorversion}.init
install -m 755 pgpool-II-%{pgmajorversion}.init %{buildroot}%{_initrddir}/pgpool-II-%{pgmajorversion}
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/pgpool-II-%{pgmajorversion}

# nuke libtool archive and static lib
rm -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

%clean
rm -rf %{buildroot}

%post
# Create alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_pool_status pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_promote_node pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node 920
%{_sbindir}/update-alternatives --install /usr/bin/pcp_systemdb_info pgpool-pcp_systemdb_info %{pgpoolinstdir}/bin/cp_systemdb_info 920
%{_sbindir}/update-alternatives --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 920

%preun
if [ $1 = 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	chkconfig --del %{sname}-%{pgmajorversion}
fi

%postun
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
%{pgpoolinstdir}/man/man8/pgpool.8
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{pgpoolinstdir}/share/pgpool-II/system_db.sql
%{_initrddir}/%{sname}-%{pgmajorversion}
%{_sysconfdir}/sysconfig/%{sname}-%{pgmajorversion}

%files devel
%defattr(-,root,root,-)
%{pgpoolinstdir}/include/libpcp_ext.h
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_type.h
%{pgpoolinstdir}/include/pool_process_reporting.h

%changelog
* Fri Aug 16 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0
- Compile pgpool with OpenSSL support, per #44
- Trim changelog
