%global	pginstdir /usr/pgsql-9.5
%global	pgmajorversion 95
%global	stinstdir /usr/%{name}
%global	sname	skytools

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		%{sname}-%{pgmajorversion}
Version:	3.2
Release:	4%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/3622/%{sname}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://pgfoundry.org/projects/skytools
BuildRequires:	postgresql%{pgmajorversion}-devel, python-devel
Requires:	python-psycopg2, postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Database management tools from Skype:WAL shipping, queueing, replication.
The tools are named walmgr, PgQ and Londiste, respectively.

%package modules
Summary:	PostgreSQL modules of Skytools
Group:		Applications/Databases
Requires:	%{sname}-%{pgmajorversion} = %{version}-%{release}

%description modules
This package has PostgreSQL modules of skytools.

%prep
%setup -q -n %{sname}-%{version}

%build
%configure --with-pgconfig=%{pginstdir}/bin/pg_config --prefix=%{stinstdir} \
	--with-python=%{_bindir}/python

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make %{?_smp_mflags} DESTDIR=%{buildroot} python-install modules-install

%clean
rm -rf %{buildroot}

%post
useradd -r skytools
mkdir -p %{_logdir}/%{name}
chown -R skytools %{_logdir}/%{name}
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_bindir}/pgqd
%{stinstdir}/bin/
%{pginstdir}/share/contrib/londiste.sql
%{pginstdir}/share/contrib/londiste.upgrade.sql
%{pginstdir}/share/contrib/newgrants_*.sql
%{pginstdir}/share/contrib/oldgrants_*.sql
%{pginstdir}/share/contrib/pgq.upgrade.sql
%{pginstdir}/share/contrib/pgq_coop.sql
%{pginstdir}/share/contrib/pgq_coop.upgrade.sql
%{pginstdir}/share/contrib/pgq_ext.sql
%{pginstdir}/share/contrib/pgq_ext.upgrade.sql
%{pginstdir}/share/contrib/pgq_node.sql
%{pginstdir}/share/contrib/pgq_node.upgrade.sql
%{pginstdir}/share/contrib/txid.sql
%{pginstdir}/share/contrib/uninstall_pgq.sql
%{pginstdir}/share/contrib/pgq.sql
%{pginstdir}/share/extension/londiste.control
%{pginstdir}/share/extension/londiste*.sql
%{pginstdir}/share/extension/pgq-*.sql
%{pginstdir}/share/extension/pgq.control
%{pginstdir}/share/extension/pgq_coop-*.sql
%{pginstdir}/share/extension/pgq_coop.control
%{pginstdir}/share/extension/pgq_node-*.sql
%{pginstdir}/share/extension/pgq_node.control
%{pginstdir}/share/extension/pgq_ext-*.sql
%{pginstdir}/share/extension/pgq_ext.control
%{_mandir}/man1/londiste3.1.gz
%{_mandir}/man1/pgqd.1.gz
%{_mandir}/man1/qadmin.1.gz
%{_mandir}/man1/queue_mover3.1.gz
%{_mandir}/man1/queue_splitter3.1.gz
%{_mandir}/man1/scriptmgr3.1.gz
%{_mandir}/man1/simple_consumer3.1.gz
%{_mandir}/man1/simple_local_consumer3.1.gz
%{_mandir}/man1/skytools_upgrade3.1.gz
%{_mandir}/man1/walmgr3.1.gz
%{stinstdir}/lib/python2.7/site-packages/pkgloader-1.0-py2.7.egg-info
%{stinstdir}/lib64/python2.7/site-packages/skytools-3.2-py2.7.egg-info
%{stinstdir}/lib/python2.7/site-packages/pkgloader.py
%{stinstdir}/lib/python2.7/site-packages/pkgloader.pyc
%{stinstdir}/lib/python2.7/site-packages/pkgloader.pyo
%{stinstdir}/lib64/python2.7/site-packages/londiste/
%{stinstdir}/lib64/python2.7/site-packages/pgq/
%{stinstdir}/lib64/python2.7/site-packages/skytools/
%{stinstdir}/share/doc/skytools3/conf/
%{stinstdir}/share/skytools3
/usr/share/doc/pgsql/extension/README.pgq
/usr/share/doc/pgsql/extension/README.pgq_ext

%files modules
%{pginstdir}/lib/pgq_lowlevel.so
%{pginstdir}/share/contrib/pgq_lowlevel.sql
%{pginstdir}/lib/pgq_triggers.so
%{pginstdir}/share/contrib/pgq_triggers.sql

%changelog
* Mon Jan 19 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.2.0-2
- Update changelog for:
   Update to 3.2, per changes described at
   http://pgfoundry.org/frs/shownotes.php?release_id=2078
- Simplify the spec file a bit
- Create unified spec file for all distros, with help of some macros.

* Tue Aug 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5, per changes described at
  http://pgfoundry.org/frs/shownotes.php?release_id=2045

* Tue Jan 15 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Fri Jul 27 2012 - Devrim Gunduz <devrim@gunduz.org> - 3.1-1
- Update to 3.1
- Re-add mistakenly removed modules subpackage

* Fri Jun 8 2012 - Devrim Gunduz <devrim@gunduz.org> - 3.0.3-1
- Update to 3.0.3

* Tue Mar 8 2011 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.12-1
- Update to 2.1.12

* Thu Mar 11 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.11-1
- Update to 2.1.11
- Apply fixes for multiple PostgreSQL installation.
- Trim changelog
