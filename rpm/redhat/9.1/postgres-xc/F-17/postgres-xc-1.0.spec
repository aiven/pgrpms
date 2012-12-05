# This spec file and ancilliary files are licensed in accordance with The 
# PostgreSQL license.

# Copyright 2012 Devrim GÜNDÜZ <devrim@gunduz.org>
# and others listed.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

# This is a macro to be used with find_lang and other stuff
%define majorversion 1.0
%define pgmajorversion 9.1
%define packageversion 10
%define oname postgres-xc
%define	pgxcbaseinstdir	/usr/pgxc-%{majorversion}

%{!?test:%define test 0}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}
%{!?selinux:%define selinux 0}

Summary:	Postgres-XC client programs and libraries
Name:		%{oname}%{packageversion}
Version:	1.0.1
Release:	1PGDG%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://www.postgres-xc.org/ 

Source0:        http://downloads.sourceforge.net/pgxc-v%{version}.tar.gz
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source9:	pgxc-1.0-libs.conf
Source12:	http://www.postgres-xc.org/docs/pdf/%{oname}-%{majorversion}-A4.pdf
Source14:	pgxc.pam
Source16:	filter-requires-perl-Pg.sh
Source17:	pgxc%{packageversion}-setup
Source18:	pgxc-%{majorversion}.service

Patch1:		rpm-pgsql.patch
Patch3:		pgxc-logging.patch
Patch6:		pgxc-perl-rpath.patch

Buildrequires:	perl glibc-devel bison flex >= 2.5.31
Requires:	/sbin/ldconfig 

%if %plperl
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	perl(ExtUtils::MakeMaker) 
%endif

%if %plpython
BuildRequires:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %uuid
BuildRequires:	uuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

%if %selinux
BuildRequires: libselinux >= 2.0.93
BuildRequires: selinux-policy >= 3.9.13
%endif

Requires:	%{name}-libs = %{version}-%{release}
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

BuildRequires:	systemd-units

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Postgres-XC is an advanced Object-Relational database management system (DBMS).
The base Postgres-XC package contains the client programs that you'll need to
access a Postgres-XC DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
Postgres-XC server, or on a remote machine that accesses a Postgres-XC server
over a network connection.  The Postgres-XC server can be found in the
postgres-xc-server sub-package.

If you want to manipulate a Postgres-XC database on a local or remote Postgres-XC
server, you need this package. You also need to install this package
if you're installing the pgxc10-server package.

%package libs
Summary:	The shared libraries required for any Postgres-XC clients
Group:		Applications/Databases
Provides:	libpq.so

%description libs
The pgxc10-libs package provides the essential shared libraries for any
Postgres-XC client program or interface. You will need to install this package
to use any other Postgres-XC package or any clients that need to connect to a
Postgres-XC server.

%package server
Summary:	The programs needed to create and run a Postgres-XC server
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):	/usr/sbin/useradd
# pre/post stuff needs systemd too
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

Requires:	%{name} = %{version}-%{release}

%description server
Postgres-XC is an advanced Object-Relational database management system (DBMS).
The pgxc10-server package contains the programs needed to create
and run a Postgres-XC server, which will in turn allow you to create
and maintain Postgres-XC databases.

%package docs
Summary:	Extra documentation for Postgres-XC
Group:		Applications/Databases

%description docs
The pgxc10-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the Postgres-XC documentation
project, or if you want to generate printed documentation. This package also 
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with Postgres-XC
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description contrib
The postgres-xc-contrib package contains various extension modules that are
included in the Postgres-XC distribution.

%package devel
Summary:	Postgres-XC development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The pgxc10-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a Postgres-XC database management server.  It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a Postgres-XC server.

%package gtm
Summary:	Global Transaction Manager for Postgres-XC
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description gtm
The pgxc10-gtm package contains gtm binaries.

%if %plperl
%package plperl
Summary:	The Perl procedural language for Postgres-XC
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Obsoletes:	pgxc10-pl

%description plperl
The pgxc10-plperl package contains the PL/Perl procedural language,
which is an extension to the Postgres-XC database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for Postgres-XC
Group:		Applications/Databases
Requires: 	%{name}%{?_isa} = %{version}-%{release}
Requires: 	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl

%description plpython
The pgxc10-plpython package contains the PL/Python procedural language,
which is an extension to the Postgres-XC database server.
Install this if you want to write database functions in Python.

%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for Postgres-XC
Group:		Applications/Databases
Requires:	%{name}-%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl

%description pltcl
Postgres-XC is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with Postgres-XC
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description test
The Postgres-XC-test package contains files needed for various tests for the
Postgres-XC database management system, including regression tests and
benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q -n pgxc
%patch1 -p1
%patch3 -p1
# patch5 is applied later
%patch6 -p1

cp -p %{SOURCE12} .

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
        if [ x"`id -u`" = x0 ]; then
               	echo "postgresql's regression tests fail if run as root."
                echo "If you really need to build the RPM as root, use"
                echo "--define='runselftest 0' to skip the regression tests."
                exit 1
        fi
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
# Add LINUX_OOM_ADJ=0 to ensure child processes reset postmaster's oom_adj
CFLAGS="$CFLAGS -DLINUX_OOM_ADJ=0"

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

# Use --as-needed to eliminate unnecessary link dependencies.
# Hopefully upstream will do this for itself in some future release.
LDFLAGS="-Wl,--as-needed"; export LDFLAGS

export LIBNAME=%{_lib}
./configure --enable-rpath \
	--prefix=%{pgxcbaseinstdir} \
	--includedir=%{pgxcbaseinstdir}/include \
	--mandir=%{pgxcbaseinstdir}/share/man \
	--datadir=%{pgxcbaseinstdir}/share \
	--libdir=%{pgxcbaseinstdir}/lib/ \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgxc \
	--docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgxcbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	cp ../../../contrib/spi/refint.so .
	cp ../../../contrib/spi/autoinc.so .
	make MAX_CONNECTIONS=5 check
	make clean
	popd
	pushd src/pl
	make MAX_CONNECTIONS=5 check
	popd
	pushd contrib
	make MAX_CONNECTIONS=5 check
	popd
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{pgxcbaseinstdir}/share/extension/
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		mv %{buildroot}%{pgxcbaseinstdir}/include/pg_config.h %{buildroot}%{pgxcbaseinstdir}/include/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgxcbaseinstdir}/include/
		#mv %{buildroot}%{pgxcbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgxcbaseinstdir}/include/server/pg_config_`uname -i`.h
		#install -m 644 %{SOURCE5} %{buildroot}%{pgxcbaseinstdir}/include/server/
		mv %{buildroot}%{pgxcbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgxcbaseinstdir}/include/ecpg_config_`uname -i`.h
		install -m 644 %{SOURCE7} %{buildroot}%{pgxcbaseinstdir}/include/
		;;
	*)
	;;
esac

# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
        -e 's|^PGENGINE=.*$|PGENGINE=/usr/pgxc-%{majorversion}/bin|' \
        <%{SOURCE17} >pgxc%{packageversion}-setup
install -m 755 pgxc%{packageversion}-setup %{buildroot}%{pgxcbaseinstdir}/bin/pgxc%{packageversion}-setup

install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/pgxc-%{majorversion}.service

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/pgxc%{packageversion}
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgxc/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgxc/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgxc/%{majorversion}

# Install a file under /etc/ld.so.conf.d, so libs can be detected easily.
install -d -m 755 %{buildroot}/etc/ld.so.conf.d/
install -m 700 %{SOURCE9} %{buildroot}/etc/ld.so.conf.d/

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pgxcbaseinstdir}/lib/test
	cp -a src/test/regress %{buildroot}%{pgxcbaseinstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pgxcbaseinstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgxcbaseinstdir}/lib/test/regress
	pushd  %{buildroot}%{pgxcbaseinstdir}/lib/test/regress
	strip *.so
	rm -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	cp %{SOURCE4} %{buildroot}%{pgxcbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgxcbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgxcbaseinstdir}/share/doc/html
mv doc-xc/src/sgml/html doc
mkdir -p %{buildroot}%{pgxcbaseinstdir}/share/man/
mv doc-xc/src/sgml/man1 doc-xc/src/sgml/man3 doc-xc/src/sgml/man7  %{buildroot}%{pgxcbaseinstdir}/share/man/
rm -rf %{buildroot}%{_docdir}/pgxc

# Temp measure for some lib files. This needs to be fixed upstream: 
mv %{buildroot}%{pgxcbaseinstdir}/lib/pgxc/* %{buildroot}%{pgxcbaseinstdir}/lib/

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

%if %nls
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetxlog-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%if %plperl
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgmajorversion}
%if %plpython
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang > pg_plpython.lst
%endif
%if %pltcl
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}
%endif

cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst
cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang > pg_devel.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetxlog-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang > pg_server.lst

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -r pgxc >/dev/null 2>&1 || :
useradd -m -g pgxc -r -s /bin/bash \
        -c "pgxc Server" pgxc >/dev/null 2>&1 || :

%post server
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
# pgxc' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgxc/1.0/data
export PGDATA" >  /var/lib/pgxc/.bash_profile
chown pgxc: /var/lib/pgxc/.bash_profile

%preun server
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable pgxc-1.0.service >/dev/null 2>&1 || :
	/bin/systemctl stop pgxc-1.0.service >/dev/null 2>&1 || :
fi

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart pgxc-1.0.service >/dev/null 2>&1 || :
fi

%if %plperl
%post 	-p /sbin/ldconfig	plperl
%postun	-p /sbin/ldconfig 	plperl
%endif

%if %plpython
%post 	-p /sbin/ldconfig	plpython
%postun	-p /sbin/ldconfig 	plpython
%endif

%if %pltcl
%post 	-p /sbin/ldconfig	pltcl
%postun	-p /sbin/ldconfig 	pltcl
%endif

%if %test
%post test
chown -R pgxc:pgxc /usr/share/pgxc/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql pgxc-psql %{pgxcbaseinstdir}/bin/psql 100
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb  pgxc-clusterdb  %{pgxcbaseinstdir}/bin/clusterdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createdb   pgxc-createdb   %{pgxcbaseinstdir}/bin/createdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createlang pgxc-createlang %{pgxcbaseinstdir}/bin/createlang 100
%{_sbindir}/update-alternatives --install /usr/bin/createuser pgxc-createuser %{pgxcbaseinstdir}/bin/createuser 100
%{_sbindir}/update-alternatives --install /usr/bin/dropdb     pgxc-dropdb     %{pgxcbaseinstdir}/bin/dropdb 100
%{_sbindir}/update-alternatives --install /usr/bin/droplang   pgxc-droplang   %{pgxcbaseinstdir}/bin/droplang 100
%{_sbindir}/update-alternatives --install /usr/bin/dropuser   pgxc-dropuser   %{pgxcbaseinstdir}/bin/dropuser 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump    pgxc-pg_dump    %{pgxcbaseinstdir}/bin/pg_dump 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall pgxc-pg_dumpall %{pgxcbaseinstdir}/bin/pg_dumpall 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore pgxc-pg_restore %{pgxcbaseinstdir}/bin/pg_restore 100
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb  pgxc-reindexdb  %{pgxcbaseinstdir}/bin/reindexdb 100
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb   pgxc-vacuumdb   %{pgxcbaseinstdir}/bin/vacuumdb 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1  pgxc-clusterdbman     %{pgxcbaseinstdir}/share/man/man1/clusterdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1   pgxc-createdbman	  %{pgxcbaseinstdir}/share/man/man1/createdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 pgxc-createlangman    %{pgxcbaseinstdir}/share/man/man1/createlang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 pgxc-createuserman    %{pgxcbaseinstdir}/share/man/man1/createuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1     pgxc-dropdbman        %{pgxcbaseinstdir}/share/man/man1/dropdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   pgxc-droplangman	  %{pgxcbaseinstdir}/share/man/man1/droplang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   pgxc-dropuserman	  %{pgxcbaseinstdir}/share/man/man1/dropuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    pgxc-pg_dumpman	  %{pgxcbaseinstdir}/share/man/man1/pg_dump.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 pgxc-pg_dumpallman    %{pgxcbaseinstdir}/share/man/man1/pg_dumpall.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 pgxc-pg_restoreman    %{pgxcbaseinstdir}/share/man/man1/pg_restore.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1	   pgxc-psqlman          %{pgxcbaseinstdir}/share/man/man1/psql.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  pgxc-reindexdbman     %{pgxcbaseinstdir}/share/man/man1/reindexdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   pgxc-vacuumdbman	  %{pgxcbaseinstdir}/share/man/man1/vacuumdb.1 100

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
        # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgxc-psql		%{pgxcbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgxc-clusterdb	%{pgxcbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgxc-clusterdbman	%{pgxcbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgxc-createdb		%{pgxcbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgxc-createdbman	%{pgxcbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgxc-createlang	%{pgxcbaseinstdir}/bin/createlang
	%{_sbindir}/update-alternatives --remove pgxc-createlangman	%{pgxcbaseinstdir}/share/man/man1/createlang.1
	%{_sbindir}/update-alternatives --remove pgxc-createuser	%{pgxcbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgxc-createuserman	%{pgxcbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgxc-dropdb		%{pgxcbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgxc-dropdbman	%{pgxcbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgxc-droplang		%{pgxcbaseinstdir}/bin/droplang
	%{_sbindir}/update-alternatives --remove pgxc-droplangman	%{pgxcbaseinstdir}/share/man/man1/droplang.1
	%{_sbindir}/update-alternatives --remove pgxc-dropuser		%{pgxcbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgxc-dropuserman	%{pgxcbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgxc-pg_dump		%{pgxcbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgxc-pg_dumpall	%{pgxcbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgxc-pg_dumpallman	%{pgxcbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgxc-pg_dumpman	%{pgxcbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgxc-pg_restore	%{pgxcbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgxc-pg_restoreman	%{pgxcbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgxc-psqlman		%{pgxcbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgxc-reindexdb	%{pgxcbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgxc-reindexdbman	%{pgxcbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgxc-vacuumdb		%{pgxcbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgxc-vacuumdbman	%{pgxcbaseinstdir}/share/man/man1/vacuumdb.1
fi

%clean
rm -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pgxcbaseinstdir}/bin/clusterdb
%{pgxcbaseinstdir}/bin/createdb
%{pgxcbaseinstdir}/bin/createlang
%{pgxcbaseinstdir}/bin/createuser
%{pgxcbaseinstdir}/bin/dropdb
%{pgxcbaseinstdir}/bin/droplang
%{pgxcbaseinstdir}/bin/dropuser
%{pgxcbaseinstdir}/bin/makesgml
%{pgxcbaseinstdir}/bin/pg_basebackup
%{pgxcbaseinstdir}/bin/pg_config
%{pgxcbaseinstdir}/bin/pg_dump
%{pgxcbaseinstdir}/bin/pg_dumpall
%{pgxcbaseinstdir}/bin/pg_restore
%{pgxcbaseinstdir}/bin/pg_test_fsync
%{pgxcbaseinstdir}/bin/psql
%{pgxcbaseinstdir}/bin/reindexdb
%{pgxcbaseinstdir}/bin/vacuumdb
%{pgxcbaseinstdir}/share/man/man1/clusterdb.*
%{pgxcbaseinstdir}/share/man/man1/createdb.*
%{pgxcbaseinstdir}/share/man/man1/createlang.*
%{pgxcbaseinstdir}/share/man/man1/createuser.*
%{pgxcbaseinstdir}/share/man/man1/dropdb.*
%{pgxcbaseinstdir}/share/man/man1/droplang.*
%{pgxcbaseinstdir}/share/man/man1/dropuser.*
%{pgxcbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgxcbaseinstdir}/share/man/man1/pg_config.*
%{pgxcbaseinstdir}/share/man/man1/pg_dump.*
%{pgxcbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgxcbaseinstdir}/share/man/man1/pg_restore.*
%{pgxcbaseinstdir}/share/man/man1/psql.*
%{pgxcbaseinstdir}/share/man/man1/reindexdb.*
%{pgxcbaseinstdir}/share/man/man1/vacuumdb.*
%{pgxcbaseinstdir}/share/man/man3/*
%{pgxcbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc-xc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%{pgxcbaseinstdir}/lib/_int.so
%{pgxcbaseinstdir}/lib/adminpack.so
%{pgxcbaseinstdir}/lib/auth_delay.so
%{pgxcbaseinstdir}/lib/autoinc.so
%{pgxcbaseinstdir}/lib/auto_explain.so
%{pgxcbaseinstdir}/lib/btree_gin.so
%{pgxcbaseinstdir}/lib/btree_gist.so
%{pgxcbaseinstdir}/lib/chkpass.so
%{pgxcbaseinstdir}/lib/citext.so
%{pgxcbaseinstdir}/lib/cube.so
%{pgxcbaseinstdir}/lib/dblink.so
%{pgxcbaseinstdir}/lib/dummy_seclabel.so
%{pgxcbaseinstdir}/lib/earthdistance.so
%{pgxcbaseinstdir}/lib/file_fdw.so*
%{pgxcbaseinstdir}/lib/fuzzystrmatch.so
%{pgxcbaseinstdir}/lib/insert_username.so
%{pgxcbaseinstdir}/lib/isn.so
%{pgxcbaseinstdir}/lib/hstore.so
%{pgxcbaseinstdir}/lib/passwordcheck.so
%{pgxcbaseinstdir}/lib/pg_freespacemap.so
%{pgxcbaseinstdir}/lib/pg_stat_statements.so
%{pgxcbaseinstdir}/lib/pgrowlocks.so
%{pgxcbaseinstdir}/lib/sslinfo.so
%{pgxcbaseinstdir}/lib/lo.so
%{pgxcbaseinstdir}/lib/ltree.so
%{pgxcbaseinstdir}/lib/moddatetime.so
%{pgxcbaseinstdir}/lib/pageinspect.so
%{pgxcbaseinstdir}/lib/pgcrypto.so
%{pgxcbaseinstdir}/lib/pgstattuple.so
%{pgxcbaseinstdir}/lib/pg_buffercache.so
%{pgxcbaseinstdir}/lib/pg_trgm.so
%{pgxcbaseinstdir}/lib/pg_upgrade_support.so
%{pgxcbaseinstdir}/lib/refint.so
%{pgxcbaseinstdir}/lib/seg.so
%{pgxcbaseinstdir}/lib/tablefunc.so
%{pgxcbaseinstdir}/lib/timetravel.so
%{pgxcbaseinstdir}/lib/unaccent.so
%if %xml
%{pgxcbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgxcbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgxcbaseinstdir}/share/pgxc/extension/
%{pgxcbaseinstdir}/bin/oid2name
%{pgxcbaseinstdir}/bin/pgbench
%{pgxcbaseinstdir}/bin/pgxc_clean
%{pgxcbaseinstdir}/bin/vacuumlo
%{pgxcbaseinstdir}/bin/pg_archivecleanup
%{pgxcbaseinstdir}/bin/pg_standby
%{pgxcbaseinstdir}/bin/pg_upgrade

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/lib/libpq.so.*
%{pgxcbaseinstdir}/lib/libecpg.so*
%{pgxcbaseinstdir}/lib/libpgtypes.so.*
%{pgxcbaseinstdir}/lib/libecpg_compat.so.*
%{pgxcbaseinstdir}/lib/libpqwalreceiver.so

%config(noreplace) %{_sysconfdir}/ld.so.conf.d/pgxc-%{majorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%{_unitdir}/pgxc-%{majorversion}.service
%{pgxcbaseinstdir}/bin/pgxc%{packageversion}-setup
%if %pam
%config(noreplace) /etc/pam.d/pgxc%{packageversion}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgxc
%{pgxcbaseinstdir}/bin/initdb
%{pgxcbaseinstdir}/bin/pg_controldata
%{pgxcbaseinstdir}/bin/pg_ctl
%{pgxcbaseinstdir}/bin/pg_resetxlog
%{pgxcbaseinstdir}/bin/postgres
%{pgxcbaseinstdir}/bin/postmaster
%{pgxcbaseinstdir}/share/man/man1/initdb.*
%{pgxcbaseinstdir}/share/man/man1/pg_controldata.*
%{pgxcbaseinstdir}/share/man/man1/pg_ctl.*
%{pgxcbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgxcbaseinstdir}/share/man/man1/postgres.*
%{pgxcbaseinstdir}/share/man/man1/postmaster.*
%{pgxcbaseinstdir}/share/pgxc/postgres.bki
%{pgxcbaseinstdir}/share/pgxc/postgres.description
%{pgxcbaseinstdir}/share/pgxc/postgres.shdescription
%{pgxcbaseinstdir}/share/pgxc/system_views.sql
%{pgxcbaseinstdir}/share/pgxc/*.sample
%{pgxcbaseinstdir}/share/pgxc/timezonesets/*
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.affix
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.dict
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.ths
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.rules
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.stop
%{pgxcbaseinstdir}/share/pgxc/tsearch_data/*.syn
%{pgxcbaseinstdir}/lib/dict_int.so
%{pgxcbaseinstdir}/lib/dict_snowball.so
%{pgxcbaseinstdir}/lib/dict_xsyn.so
%{pgxcbaseinstdir}/lib/euc2004_sjis2004.so
%{pgxcbaseinstdir}/lib/plpgsql.so
%dir %{pgxcbaseinstdir}/share/extension
#%{pgxcbaseinstdir}/share/extension/plpgsql*
%{pgxcbaseinstdir}/lib/test_parser.so
%{pgxcbaseinstdir}/lib/tsearch2.so

%dir %{pgxcbaseinstdir}/lib
%dir %{pgxcbaseinstdir}/share
%attr(700,pgxc,pgxc) %dir /var/lib/pgxc
%attr(700,pgxc,pgxc) %dir /var/lib/pgxc/%{majorversion}
%attr(700,pgxc,pgxc) %dir /var/lib/pgxc/%{majorversion}/data
%attr(700,pgxc,pgxc) %dir /var/lib/pgxc/%{majorversion}/backups
#%attr(644,pgxc,pgxc) %config(noreplace) /var/lib/pgxc/.bash_profile
%{pgxcbaseinstdir}/lib/*_and_*.so
%{pgxcbaseinstdir}/share/pgxc/conversion_create.sql
%{pgxcbaseinstdir}/share/pgxc/information_schema.sql
%{pgxcbaseinstdir}/share/pgxc/snowball_create.sql
%{pgxcbaseinstdir}/share/pgxc/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/include/*
%{pgxcbaseinstdir}/bin/ecpg
%{pgxcbaseinstdir}/lib/libpq.so
%{pgxcbaseinstdir}/lib/libecpg.so
%{pgxcbaseinstdir}/lib/libpq.a
%{pgxcbaseinstdir}/lib/libecpg.a
%{pgxcbaseinstdir}/lib/libecpg_compat.so
%{pgxcbaseinstdir}/lib/libecpg_compat.a
%{pgxcbaseinstdir}/lib/libpgport.a
%{pgxcbaseinstdir}/lib/libpgtypes.so
%{pgxcbaseinstdir}/lib/libpgtypes.a
%{pgxcbaseinstdir}/lib/pgxs/*
%{pgxcbaseinstdir}/share/man/man1/ecpg.*

%files gtm -f pg_devel.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/bin/gtm
%{pgxcbaseinstdir}/bin/gtm_ctl
%{pgxcbaseinstdir}/bin/gtm_proxy
%{pgxcbaseinstdir}/bin/initgtm
%{pgxcbaseinstdir}/share/man/man1/gtm.1
%{pgxcbaseinstdir}/share/man/man1/gtm_ctl.1
%{pgxcbaseinstdir}/share/man/man1/gtm_proxy.1
%{pgxcbaseinstdir}/share/man/man1/initgtm.1

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/lib/plperl.so
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/lib/pltcl.so
%{pgxcbaseinstdir}/bin/pltcl_delmod
%{pgxcbaseinstdir}/bin/pltcl_listmod
%{pgxcbaseinstdir}/bin/pltcl_loadmod
%{pgxcbaseinstdir}/share/pgxc/unknown.pltcl
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgxcbaseinstdir}/lib/plpython*.so
%endif

%if %test
%files test
%defattr(-,pgxc,pgxc)
%attr(-,pgxc,pgxc) %{pgxcbaseinstdir}/lib/test/*
%attr(-,pgxc,pgxc) %dir %{pgxcbaseinstdir}/lib/test
%endif

%changelog
* Wed Sep 5 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.1-1PGDG
- Update to 1.0.1

* Mon Sep 03 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-2PGDG
- Remove useless ldconfig call from -server subpackage.

* Mon Aug 13 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial cut for 1.0.0
