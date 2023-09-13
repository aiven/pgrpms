%global	debug_package %{nil}
%global _slonconffilter /etc/slon_tools.conf
%global __requires_exclude ^(%{_slonconffilter})$
%global sname slony1
%global slonymajorversion 22
%{!?docs:%global docs 0}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.11
Release:	2PGDG%{?dist}
License:	BSD
URL:		https://www.slony.info/
Source0:	http://main.slony.info/downloads/2.2/source/%{sname}-%{version}.tar.bz2
Source2:	%{sname}-%{slonymajorversion}-filter-requires-perl-Pg.sh
Source5:	%{sname}-%{slonymajorversion}-%{pgmajorversion}.service
Source6:	%{sname}-%{slonymajorversion}-%{pgmajorversion}-tmpfiles.d
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}-server
BuildRequires:	flex pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server perl-DBD-Pg
Conflicts:	slony1

BuildRequires:		systemd systemd-devel
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

Obsoletes:	%{sname}-%{pgmajorversion} < 2.2.8-3

%if %docs
BuildRequires:	docbook-style-dsssl postgresql_autodoc docbook-utils
%endif

%description
Slony-I is a "master to multiple slaves" replication
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Requires:	%{sname}-%{pgmajorversion}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript

%description docs
The slony1-docs package includes some documentation for Slony-I.
%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}
%build

# Fix permissions of docs.
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%else
	CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
	CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
	CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
	CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
export LIBNAME=%{_lib}
%endif
%configure --prefix=%{pginstdir} --includedir %{pginstdir}/include --with-pgconfigdir=%{pginstdir}/bin --libdir=%{pginstdir}/lib \
	--with-perltools=%{pginstdir}/bin --sysconfdir=%{_sysconfdir}/%{sname}-%{pgmajorversion} \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{sname}-%{version} \
%endif
	--datadir=%{pginstdir}/share --with-pglibdir=%{pginstdir}/lib

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} -C tools

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample slon.conf file
%{__install} -d %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}
%{__install} -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon.conf
%{__install} -m 0644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf

# Fix the log path
sed "s:\([$]LOGDIR = '/var/log/slony1\):\1-%{pgmajorversion}:" -i %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf

# change file modes of docs.
%{__chmod} 644 COPYRIGHT UPGRADING SAMPLE RELEASE


# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/
# ... and make a tmpfiles script to recreate it at reboot.
%{__install} -d -m 755 %{buildroot}/%{_rundir}/%{name}
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE6} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

cd tools
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install shell scripts
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__cp} check_slon.sh check_slony_cluster.sh configure-replication.sh duplicate-node.sh \
	find-triggers-to-deactivate.sh generate_syncs.sh launch_clusters.sh mkslonconf.sh \
	run_rep_tests.sh search-logs.sh slonikconfdump.sh slony-cluster-analysis-mass.sh \
	slony-cluster-analysis.sh slony1_dump.sh slony1_extract_schema.sh %{buildroot}%{_datadir}/%{name}/
# Perform some cleanup
%{__rm} -f %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf-sample
%{__rm} -f %{buildroot}%{_datadir}/pgsql/*.sql
%{__rm} -f %{buildroot}%{_libdir}/slony1_funcs.so

%post
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{sname}-%{slonymajorversion}-%{pgmajorversion}.service
   %endif
   %else
   %systemd_post %{sname}-%{slonymajorversion}-%{pgmajorversion}.service
   %endif
fi
if [ ! -e "/var/log/slony1-%{pgmajorversion}" -a ! -h "/var/log/slony1-%{pgmajorversion}" ]
then
	%{__mkdir} /var/log/slony1-%{pgmajorversion}
	%{__chown} postgres:postgres /var/log/slony1-%{pgmajorversion}
fi
if [ ! -e "/run/slony1-%{pgmajorversion}/" -a ! -h "/run/slony1-%{pgmajorversion}/" ]
then
	%{__mkdir} /run/slony1-%{pgmajorversion}
	%{__chown} postgres:postgres /run/slony1-%{pgmajorversion}
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}-%{slonymajorversion}-%{pgmajorversion} >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}-%{slonymajorversion}-%{pgmajorversion} >/dev/null 2>&1 || :
fi


%postun
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
# Package upgrade, not uninstall
/bin/systemctl try-restart %{sname}-%{slonymajorversion}-%{pgmajorversion} >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING INSTALL SAMPLE RELEASE
%{pginstdir}/bin/slon*
%{pginstdir}/lib/slon*
%{pginstdir}/share/slon*
%{_datadir}/%{name}/*.sh
%config(noreplace) %{_sysconfdir}/%{sname}-%{pgmajorversion}/slon.conf
%config(noreplace) %{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf
%ghost %{_rundir}
%{_tmpfilesdir}/%{name}.conf
%attr (644, root, root) %{_unitdir}/%{sname}-%{slonymajorversion}-%{pgmajorversion}.service

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide doc/concept doc/howto doc/implementation doc/support
%endif

%changelog
* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.11-2PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 3 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.11-1
- Update to 2.2.11
- Remove RHEL 6 bits.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.10-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Dec 8 2020 Devrim Gündüz <devrim@gunduz.org> - 2.2.10-1
- Update to 2.2.10

* Wed Dec 2 2020 Devrim Gündüz <devrim@gunduz.org> - 2.2.9-1
- Update to 2.2.9

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.2.8-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.8-2
- Fix RHEL 6 packaging. Patch from Sandeep Thakkar.

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.8-1.1
- Rebuild for PostgreSQL 12

* Tue Aug 27 2019 - Devrim Gündüz <devrim@gunduz.org> 2.2.8-1
- Update to 2.2.8

* Sat Apr 13 2019 - Devrim Gündüz <devrim@gunduz.org> 2.2.7-4
- More fixes for the pid file location

* Sat Dec 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.2.7-3
- Fix path in tmpfiles.d drop-in file

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.7-2
- Install tools script, per #3732 .

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.7-2
- Install tools script, per #3732 .

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.7-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 21 2018 Devrim Gündüz <devrim@gunduz.org> 2.2.7-1
- Update to 2.2.7

* Sun Oct 15 2017 Devrim Gündüz <devrim@gunduz.org> 2.2.6-3
- Fix #1002.

* Sun Sep 3 2017 Devrim Gündüz <devrim@gunduz.org> 2.2.6-2
- Add systemd support

* Mon Aug 28 2017 Devrim Gündüz <devrim@gunduz.org> 2.2.6-1
- Update to 2.2.6

* Mon Jul 4 2016 Devrim Gündüz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5

* Sun Jul 5 2015 Devrim Gündüz <devrim@gunduz.org> 2.2.4-4
- Various updates to init script, per Rob Brucks.
- Cosmetic updates to spec file (using macros)

* Tue Mar 17 2015 Devrim Gündüz <devrim@gunduz.org> 2.2.4-3
- Fix the log directory, so that it points to correct release.
  Per bug report from Guillaume Lelarge.

* Mon Jan 19 2015 Devrim Gündüz <devrim@gunduz.org> 2.2.4-2
- Fix init script so that it reads the conninfo correctly.
  Per Tomonari Katsumata.
- Fix major version number in init script.

* Mon Jan 19 2015 Devrim Gündüz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Wed Jul 9 2014 Devrim Gündüz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Wed Feb 12 2014 Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sat Nov 9 2013 Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Tue Sep 10 2013 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0
- Trim changelog.

* Fri Aug 23 2013 Xavier Bergade <XavierB@benon.com> 2.1.4-2
- Set --sysconfdir during configure to fix the require list & the CONFIG_FILE path in the Perl scripts
- Set the correct path for LOGDIR in the slon_tools.conf file

* Tue Aug 20 2013 Devrim Gündüz <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Mon Jun 24 2013 Devrim Gündüz <devrim@gunduz.org> 2.1.3-2
- Various fixes for multiple postmaster feature:
 - Install slony config files in separate directories.
 - Update init scripts.
 - Install pid and log files into separate directories.
 - Properly filter dependency to /etc/slon_tools.conf
 - Use default sysconfig file, to be used by init script.

* Tue Feb 19 2013 Devrim Gündüz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3
- Fix init script names in %%postun and %%preun.

* Sat Feb 09 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.2-2
- Rebuilt.

* Sat Sep 1 2012 Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Jun 8 2012 Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1

* Wed Oct 05 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.7-2
- Use correct pgmajorversion number, per report from Ger Timmens.

* Fri Aug 12 2011 Devrim Gündüz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7.

* Thu Dec 9 2010 Devrim Gündüz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Fri Oct 8 2010 Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Sat Sep 18 2010 Devrim Gündüz <devrim@gunduz.org> 2.0.4-1
- Update to 2.0.4, and perform a major cleanup and bugfix.
- Apply changes for 9.0+
- Update source2, to supress weird dependency for slon_tools.conf.

* Sat Apr 10 2010 Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3
- Updated doc patch
- Rename log directory to slony, to match upstream default
- Apply many fixes to support multiple postmaster installation.

* Sat May 9 2009 Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2
- Removed patch0 -- it is no longer needed.
- Added a temp patch to get rid of sgml error.
- Re-enable doc builds

* Sat Mar 14 2009 Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Create log directory, per pgcore #77.

* Thu Jan 29 2009 Devrim Gündüz <devrim@gunduz.org> 2.0.0-3
- Add docbook-utils to BR.

* Sat Dec 13 2008 Devrim Gündüz <devrim@gunduz.org> 2.0.0-2
- Add a patch to fix build errors
- Temporarily update Source2, so that it will silence a dependency error.

* Tue Dec 2 2008 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
