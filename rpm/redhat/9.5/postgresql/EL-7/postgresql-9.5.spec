# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:
# but the tarball is different.

# Test releases are where PostgreSQL itself is not in beta, but certain parts of
# the RPM packaging (such as the spec file, the initscript, etc) are in beta.

# Pre-release RPM's should not be put up on the public ftp.postgresql.org server
# -- only test releases or full releases should be.
# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003-2016 Devrim GÜNDÜZ <devrim@gunduz.org>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Tom Lane
# Jeff Frost
# Peter Eisentraut
# Alvaro Herrera
# David Fetter
# Greg Smith
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%global kerbdir "/usr"}

# These are macros to be used with find_lang and other stuff
%global majorversion 9.5
%global packageversion 95
%global oname postgresql
%global	pgbaseinstdir	/usr/pgsql-%{majorversion}

# Configure parameters
%{!?disablepgfts:%global disablepgfts 0}
%{!?intdatetimes:%global intdatetimes 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}
%{!?plperl:%global plperl 1}
%{!?plpy%{!?pltcl:%global pltcl 1}
%{!?plpython:%global plpython 1}
%if 0%{?fedora} > 22
%{!?plpython3:%global plpython3 1}
%endif
%{!?runselftest:%global runselftest 0}
%{!?selinux:%global selinux 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?sdt:%global sdt 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%{!?sdt:%global sdt 1}
%endif
%if 0%{?fedora} > 22
%global _hardened_build 1
%endif

Summary:	PostgreSQL client programs and libraries
Name:		%{oname}%{packageversion}
Version:	9.5.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source9:	postgresql-%{majorversion}-libs.conf
Source12:	http://www.postgresql.org/files/documentation/pdf/%{majorversion}/%{oname}-%{majorversion}-A4.pdf
Source14:	postgresql.pam
Source16:	filter-requires-perl-Pg.sh
Source17:	postgresql%{packageversion}-setup
%if %{systemd_enabled}
Source10:	postgresql%{packageversion}-check-db-dir
Source18:	postgresql-%{majorversion}.service
Source19:	postgresql.tmpfiles.d
%else
Source3:	postgresql.init
%endif

Patch1:		rpm-pgsql.patch
Patch3:		postgresql-logging.patch
Patch5:		postgresql-var-run-socket.patch
Patch6:		postgresql-perl-rpath.patch
Patch8:		postgresql-python3.5-tests.patch

BuildRequires:	perl glibc-devel bison flex >= 2.5.31
Requires:	/sbin/ldconfig

%if %plperl
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	perl(ExtUtils::MakeMaker)
%endif

%if %plpython
BuildRequires:	python-devel
%endif

%if %plpython3
BuildRequires: python3-devel
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

%if %sdt
BuildRequires:	systemtap-sdt-devel
%endif

%if %uuid
BuildRequires:	libuuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

%if %selinux
BuildRequires: libselinux >= 2.0.93
BuildRequires: selinux-policy >= 3.9.13
%endif
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

# These are required for -docs subpackage:

BuildRequires:	openjade
BuildRequires:	opensp
BuildRequires:	docbook-dtds
BuildRequires:	docbook-style-dsssl
BuildRequires:	libxslt

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	postgresql

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.  The PostgreSQL server can be found in the
postgresql%{packageversion}-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql%{packageversion}-server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Group:		Applications/Databases
Provides:	postgresql-libs

%description libs
The postgresql%{packageversion}-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):	/usr/sbin/useradd
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc
%if %{systemd_enabled}
# pre/post stuff needs systemd too
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
%else
Requires:	/usr/sbin/useradd /sbin/chkconfig
%endif
Requires:	%{name} = %{version}-%{release}
Provides:	postgresql-server

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql%{packageversion}-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package docs
Summary:	Extra documentation for PostgreSQL
Group:		Applications/Databases
Provides:	postgresql-docs

%description docs
The postgresql%{packageversion}-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	postgresql-contrib

%description contrib
The postgresql%{packageversion}-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	postgresql-devel

%description devel
The postgresql%{packageversion}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server.  It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a PostgreSQL server.


%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Obsoletes:	postgresql%{packageversion}-pl
Provides:	postgresql-plperl

%description plperl
The postgresql%{packageversion}-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl
Provides:	postgresql-plpython

%description plpython
The postgresql%{packageversion}-plpython package contains the PL/Python procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python.

%endif

%if %plpython3
%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl
Provides:	postgresql-plpython3

%description plpython3
The postgresql%{packageversion}-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.

%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl
Provides:	postgresql-pltcl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	postgresql-test

%description test
The postgresql%{packageversion}-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%global __perl_requires %{SOURCE16}

%prep
%setup -q -n %{oname}-%{version}
%patch1 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1

%{__cp} -p %{SOURCE12} .

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

# plpython requires separate configure/build runs to build against python 2
# versus python 3.  Our strategy is to do the python 3 run first, then make
# distclean and do it again for the "normal" build.  Note that the installed
# Makefile.global will reflect the python 2 build, which seems appropriate
# since that's still considered the default plpython version.
%if %plpython3

export PYTHON=/usr/bin/python3

# These configure options must match main build
./configure --enable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
	--libdir=%{pgbaseinstdir}/lib \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython3
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
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %sdt
	--enable-dtrace \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-uuid=e2fs \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{pgbaseinstdir}/doc \
	--htmldir=%{pgbaseinstdir}/doc/html
# Fortunately we don't need to build much except plpython itself
cd src/backend
make submake-errcodes
cd ../..
cd src/pl/plpython
make %{?_smp_mflags} all
cd ..
# save built form in a directory that "make distclean" won't touch
%{__cp} -a plpython plpython3
cd ../..

# must also save this version of Makefile.global for later
%{__cp} src/Makefile.global src/Makefile.global.python3

make distclean

%endif

unset PYTHON

# Normal (not python3) build begins here
./configure --enable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
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
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %sdt
        --enable-dtrace \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-uuid=e2fs \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{pgbaseinstdir}/doc \
	--htmldir=%{pgbaseinstdir}/doc/html

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
%{__rm} -f src/tutorial/GNUmakefile


# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path.  When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.

run_testsuite()
{
	make -C "$1" MAX_CONNECTIONS=5 check && return 0

	test_failure=1

	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

%if %runselftest
	run_testsuite "src/test/regress"
	make clean -C "src/test/regress"
	run_testsuite "src/pl"
%if %plpython3
	# must install Makefile.global that selects python3
	%{__mv} src/Makefile.global src/Makefile.global.save
	%{__cp} src/Makefile.global.python3 src/Makefile.global
	touch -r src/Makefile.global.save src/Makefile.global
	# because "make check" does "make install" on the whole tree,
	# we must temporarily install plpython3 as src/pl/plpython,
	# since that is the subdirectory src/pl/Makefile knows about
	%{__mv} src/pl/plpython src/pl/plpython2
	%{__mv} src/pl/plpython3 src/pl/plpython

	run_testsuite "src/pl/plpython"

	# and clean up our mess
	%{__mv} src/pl/plpython src/pl/plpython3
	%{__mv} src/pl/plpython2 src/pl/plpython
	%{__mv} -f src/Makefile.global.save src/Makefile.global
%endif
	run_testsuite "contrib"
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
%{__rm} -rf %{buildroot}

make DESTDIR=%{buildroot} install

%if %plpython3
	%{__mv} src/Makefile.global src/Makefile.global.save
	%{__cp} src/Makefile.global.python3 src/Makefile.global
	touch -r src/Makefile.global.save src/Makefile.global
	pushd src/pl/plpython3
	make DESTDIR=%{buildroot} install
	popd
	%{__mv} -f src/Makefile.global.save src/Makefile.global
%endif

mkdir -p %{buildroot}%{pgbaseinstdir}/share/extensions/
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/
		%{__mv}  %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
		install -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/
		;;
	*)
	;;
esac

# This is only for systemd supported distros.
%if %{systemd_enabled}
# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
	-e 's|^PGENGINE=.*$|PGENGINE=/usr/pgsql-%{majorversion}/bin|' \
	<%{SOURCE17} >postgresql%{packageversion}-setup
install -m 755 postgresql%{packageversion}-setup %{buildroot}%{pgbaseinstdir}/bin/postgresql%{packageversion}-setup

# prep the startup check script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	-e 's|^PGDOCDIR=.*$|PGDOCDIR=%{_pkgdocdir}|' \
	<%{SOURCE10} >postgresql%{packageversion}-check-db-dir
touch -r %{SOURCE10} postgresql%{packageversion}-check-db-dir
install -m 755 postgresql%{packageversion}-check-db-dir %{buildroot}%{pgbaseinstdir}/bin/postgresql%{packageversion}-check-db-dir
%endif

%if %{systemd_enabled}
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/postgresql-%{majorversion}.service
%else
install -d %{buildroot}%{_initrddir}
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
install -m 755 postgresql.init %{buildroot}%{_initrddir}/postgresql-%{majorversion}
%endif

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/postgresql%{packageversion}
%endif

# Create the directory for sockets.
install -d -m 755 %{buildroot}/var/run/postgresql
%if %{systemd_enabled}
# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}/%{_tmpfilesdir}
install -m 0644 %{SOURCE19} %{buildroot}/%{_tmpfilesdir}/postgresql-%{majorversion}.conf
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{majorversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
install -d -m 755 %{buildroot}%{pgbaseinstdir}/share/
install -m 700 %{SOURCE9} %{buildroot}%{pgbaseinstdir}/share/

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pgbaseinstdir}/lib/test
	%{__cp} -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	pushd  %{buildroot}%{pgbaseinstdir}/lib/test/regress
	strip *.so
	%{__rm} -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	%{__cp} %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
%{__cp} %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgbaseinstdir}/share/doc/html
%{__mv} doc/src/sgml/html doc
mkdir -p %{buildroot}%{pgbaseinstdir}/share/man/
%{__mv} doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7  %{buildroot}%{pgbaseinstdir}/share/man/
%{__rm} -rf %{buildroot}%{_docdir}/pgsql

# initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython.lst
%{__cp} /dev/null plpython3.lst

# initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython.lst

%if %nls
%find_lang ecpg-%{majorversion}
%find_lang ecpglib6-%{majorversion}
%find_lang initdb-%{majorversion}
%find_lang libpq5-%{majorversion}
%find_lang pg_basebackup-%{majorversion}
%find_lang pg_config-%{majorversion}
%find_lang pg_controldata-%{majorversion}
%find_lang pg_ctl-%{majorversion}
%find_lang pg_dump-%{majorversion}
%find_lang pg_resetxlog-%{majorversion}
%find_lang pg_rewind-%{majorversion}
%find_lang pgscripts-%{majorversion}
%if %plperl
%find_lang plperl-%{majorversion}
cat plperl-%{majorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{majorversion}
%if %plpython
%find_lang plpython-%{majorversion}
cat plpython-%{majorversion}.lang > pg_plpython.lst
%endif
%if %plpython3
# plpython3 shares message files with plpython
%find_lang plpython-%{majorversion}
cat plpython-%{majorversion}.lang >> pg_plpython3.lst
%endif

%if %pltcl
%find_lang pltcl-%{majorversion}
cat pltcl-%{majorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{majorversion}
%find_lang psql-%{majorversion}
%endif

cat libpq5-%{majorversion}.lang > pg_libpq5.lst
cat pg_config-%{majorversion}.lang ecpg-%{majorversion}.lang ecpglib6-%{majorversion}.lang > pg_devel.lst
cat initdb-%{majorversion}.lang pg_ctl-%{majorversion}.lang psql-%{majorversion}.lang pg_dump-%{majorversion}.lang pg_basebackup-%{majorversion}.lang pg_rewind-%{majorversion}.lang pgscripts-%{majorversion}.lang > pg_main.lst
cat postgres-%{majorversion}.lang pg_resetxlog-%{majorversion}.lang pg_controldata-%{majorversion}.lang plpgsql-%{majorversion}.lang > pg_server.lst

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post postgresql-%{majorversion}.service
   %tmpfiles_createa
  %else
   chkconfig --add postgresql-%{majorversion}
  %endif
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/%{majorversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
#[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" >  /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

%preun server
if [ $1 -eq 0 ] ; then
%if %{systemd_enabled}
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable postgresql-%{majorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop postgresql-%{majorversion}.service >/dev/null 2>&1 || :
%else
	/sbin/service postgresql-%{majorversion} condstop >/dev/null 2>&1
	chkconfig --del postgresql-%{majorversion}

%endif
fi

%postun server
/sbin/ldconfig
%if %{systemd_enabled}
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 sbin/service postgresql-%{majorversion} condrestart >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %{systemd_enabled}
	# Package upgrade, not uninstall
	/bin/systemctl try-restart postgresql-%{majorversion}.service >/dev/null 2>&1 || :
 %endif
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
chown -R postgres:postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql	pgsql-psql %{pgbaseinstdir}/bin/psql %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb pgsql-clusterdb  %{pgbaseinstdir}/bin/clusterdb %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/createdb pgsql-createdb   %{pgbaseinstdir}/bin/createdb %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/createlang pgsql-createlang %{pgbaseinstdir}/bin/createlang %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/createuser pgsql-createuser %{pgbaseinstdir}/bin/createuser %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/dropdb pgsql-dropdb     %{pgbaseinstdir}/bin/dropdb %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/droplang pgsql-droplang   %{pgbaseinstdir}/bin/droplang %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/dropuser pgsql-dropuser   %{pgbaseinstdir}/bin/dropuser %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pg_basebackup pgsql-pg_basebackup    %{pgbaseinstdir}/bin/pg_basebackup %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump pgsql-pg_dump    %{pgbaseinstdir}/bin/pg_dump %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall pgsql-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore pgsql-pg_restore %{pgbaseinstdir}/bin/pg_restore %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb pgsql-reindexdb  %{pgbaseinstdir}/bin/reindexdb %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb pgsql-vacuumdb   %{pgbaseinstdir}/bin/vacuumdb %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1 pgsql-clusterdbman     %{pgbaseinstdir}/share/man/man1/clusterdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1 pgsql-createdbman	  %{pgbaseinstdir}/share/man/man1/createdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 pgsql-createlangman    %{pgbaseinstdir}/share/man/man1/createlang.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 pgsql-createuserman    %{pgbaseinstdir}/share/man/man1/createuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1	pgsql-dropdbman        %{pgbaseinstdir}/share/man/man1/dropdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   pgsql-droplangman	  %{pgbaseinstdir}/share/man/man1/droplang.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   pgsql-dropuserman	  %{pgbaseinstdir}/share/man/man1/dropuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_basebackup.1    pgsql-pg_basebackupman	  %{pgbaseinstdir}/share/man/man1/pg_basebackup.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    pgsql-pg_dumpman	  %{pgbaseinstdir}/share/man/man1/pg_dump.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 pgsql-pg_dumpallman    %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 pgsql-pg_restoreman    %{pgbaseinstdir}/share/man/man1/pg_restore.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1	   pgsql-psqlman          %{pgbaseinstdir}/share/man/man1/psql.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  pgsql-reindexdbman     %{pgbaseinstdir}/share/man/man1/reindexdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   pgsql-vacuumdbman	  %{pgbaseinstdir}/share/man/man1/vacuumdb.1 %{packageversion}0

%post libs
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/postgresql-pgdg-libs.conf   pgsql-ld-conf        %{pgbaseinstdir}/share/postgresql-%{majorversion}-libs.conf %{packageversion}0
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
        # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgsql-psql		%{pgbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgsql-clusterdb	%{pgbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgsql-clusterdbman	%{pgbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createdb		%{pgbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgsql-createdbman	%{pgbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createlang	%{pgbaseinstdir}/bin/createlang
	%{_sbindir}/update-alternatives --remove pgsql-createlangman	%{pgbaseinstdir}/share/man/man1/createlang.1
	%{_sbindir}/update-alternatives --remove pgsql-createuser	%{pgbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgsql-createuserman	%{pgbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgsql-dropdb		%{pgbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgsql-dropdbman	%{pgbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgsql-droplang		%{pgbaseinstdir}/bin/droplang
	%{_sbindir}/update-alternatives --remove pgsql-droplangman	%{pgbaseinstdir}/share/man/man1/droplang.1
	%{_sbindir}/update-alternatives --remove pgsql-dropuser		%{pgbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgsql-dropuserman	%{pgbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackup	%{pgbaseinstdir}/bin/pg_basebackup
	%{_sbindir}/update-alternatives --remove pgsql-pg_dump		%{pgbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpall	%{pgbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpallman	%{pgbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackupman	%{pgbaseinstdir}/share/man/man1/pg_basebackup.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpman	%{pgbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_restore	%{pgbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgsql-pg_restoreman	%{pgbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgsql-psqlman		%{pgbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgsql-reindexdb	%{pgbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgsql-reindexdbman	%{pgbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdb		%{pgbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdbman	%{pgbaseinstdir}/share/man/man1/vacuumdb.1
  fi

%postun libs
if [ "$1" -eq 0 ]
  then
	%{_sbindir}/update-alternatives --remove pgsql-ld-conf          %{pgbaseinstdir}/share/postgresql-%{majorversion}-libs.conf
	/sbin/ldconfig
fi

%clean
%{__rm} -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createlang
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/droplang
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_receivexlog
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_xlogdump
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createlang.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/droplang.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pgbench.1
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.1
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_isready.*
%{pgbaseinstdir}/share/man/man1/pg_receivexlog.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/pg_rewind.1
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.1
%{pgbaseinstdir}/share/man/man1/pg_test_timing.1
%{pgbaseinstdir}/share/man/man1/pg_upgrade.1
%{pgbaseinstdir}/share/man/man1/pg_xlogdump.1
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%doc %{pgbaseinstdir}/doc/extension/*.example
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/chkpass.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%if %plperl
%{pgbaseinstdir}/lib/hstore_plperl.so
%endif
%if %plpython
%{pgbaseinstdir}/lib/hstore_plpython2.so
%endif
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%if %plpython
%{pgbaseinstdir}/lib/ltree_plpython2.so
%endif
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_prewarm.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/sslinfo.so
%if %selinux
%{pgbaseinstdir}/lib/sepgsql.so
%{pgbaseinstdir}/share/contrib/sepgsql.sql
%endif
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/test_decoding.so
%{pgbaseinstdir}/lib/timetravel.so
%{pgbaseinstdir}/lib/tsm_system_rows.so
%{pgbaseinstdir}/lib/tsm_system_time.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/extension/adminpack*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/chkpass*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore*
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree*
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_prewarm*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%{pgbaseinstdir}/share/extension/sslinfo*
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/timetravel*
%{pgbaseinstdir}/share/extension/tsearch2*
%{pgbaseinstdir}/share/extension/tsm_system_rows*
%{pgbaseinstdir}/share/extension/tsm_system_time*
%{pgbaseinstdir}/share/extension/unaccent*
%if %uuid
%{pgbaseinstdir}/share/extension/uuid-ossp*
%endif
%{pgbaseinstdir}/share/extension/xml2*
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/share/man/man1/oid2name.1
%{pgbaseinstdir}/share/man/man1/pg_recvlogical.1
%{pgbaseinstdir}/share/man/man1/pg_standby.1
%{pgbaseinstdir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %{pgbaseinstdir}/share/postgresql-%{majorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%if %{systemd_enabled}
%{_tmpfilesdir}/postgresql-%{majorversion}.conf
%{_unitdir}/postgresql-%{majorversion}.service
%{pgbaseinstdir}/bin/postgresql%{packageversion}-setup
%{pgbaseinstdir}/bin/postgresql%{packageversion}-check-db-dir
%else
%config(noreplace) %{_initrddir}/postgresql-%{majorversion}
%endif
%if %pam
%config(noreplace) /etc/pam.d/postgresql%{packageversion}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/postgres.description
%{pgbaseinstdir}/share/postgres.shdescription
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/plpgsql.so
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*
%{pgbaseinstdir}/lib/tsearch2.so

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/backups
%attr(755,postgres,postgres) %dir /var/run/postgresql
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/conversion_create.sql
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plperl.so
%{pgbaseinstdir}/share/extension/plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/bin/pltcl_delmod
%{pgbaseinstdir}/bin/pltcl_listmod
%{pgbaseinstdir}/bin/pltcl_loadmod
%{pgbaseinstdir}/share/unknown.pltcl
%{pgbaseinstdir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plpython2.so
%{pgbaseinstdir}/share/extension/plpython2u*
%{pgbaseinstdir}/share/extension/plpythonu*
%endif

%if %plpython3
%files plpython3 -f pg_plpython3.lst
%{pgbaseinstdir}/share/extension/plpython3*
%{pgbaseinstdir}/lib/plpython3.so
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Mon Jan 18 2016 Devrim Gündüz <devrim@gunduz.org> - 9.5.0-2PGDG
- Unified spec file for all distros.
- Ship plpython3 subpackage. Per report from Clodoaldo Neto on
  pgsql-pkg-yum mailing list. I got all the patch from Fedora's
  postgresql package.
- Fix testsuite failure with new Python 3.5 (rhbz#1280404). Patch
  taken from Pavel Raiskup's patch on Fedora spec file.
- Fix PostgreSQL version number in tmpfiles.d file, and use macro.
- Build with dtrace support, where available.
- Use RPM macros for some of the commands.
- Sort the macros in alphabetical order.

* Mon Jan 4 2016 Devrim Gündüz <devrim@gunduz.org> - 9.5.0-1PGDG
- Update to 9.5.0

* Thu Dec 17 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5rc1-1PGDG
- Update to 9.5rc1

* Tue Nov 10 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5beta2-1PGDG
- Update to 9.5beta2
- Enable hardened build on Fedora.

* Tue Nov 3 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5beta1-2PGDG
- Specify/fix --docdir and --htmldir in configure line.

* Tue Oct 6 2015 Jeff Frost <jeff@pgexperts.com> - 9.5.beta1-1PGDG
- Update to 9.5beta1

* Thu Aug 6 2015 Jeff Frost <jeff@pgexperts.com> - 9.5.alpha2-1PGDG
- Update to 9.5alpha2

* Wed Jul 1 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5alpha1-1PGDG
- Initial cut for 9.5 alpha1
- Move pg_archivecleanup, pg_test_fsync, pg_test_timing, pg_xlogdump,
  pgbench, and pg_upgrade to main package.
- Remove dummy_seclabel, test_shm_mq, test_parser, and worker_spi.

* Thu Jun 11 2015 Devrim Gündüz <devrim@gunduz.org> - 9.4.4-1PGDG
- Update to 9.4.4, per changes described at:
  http://www.postgresql.org/docs/9.4/static/release-9-4-4.html

* Thu Jun 4 2015 Devrim Gündüz <devrim@gunduz.org> - 9.4.3-1PGDG
- Update to 9.4.3, per changes described at:
  http://www.postgresql.org/docs/9.4/static/release-9-4-3.html

* Fri May 22 2015 Devrim Gündüz <devrim@gunduz.org> - 9.4.2-2PGDG
- Create and own /var/run/postgresql directory. Per report from
  Pete Deffendol.

* Wed May 20 2015 Devrim Gündüz <devrim@gunduz.org> - 9.4.2-1PGDG
- Update to 9.4.2, per changes described at:
  http://www.postgresql.org/docs/9.4/static/release-9-4-2.html
- Add a new patch (Patch5) from Fedora:
  * Configure postmaster to create sockets in both /var/run/postgresql and /tmp;
    the former is now the default place for libpq to contact the postmaster.
- Add tmpfiles.d conf file

* Tue Feb 3 2015 Devrim Gündüz <devrim@gunduz.org> - 9.4.1-1PGDG
- Update to 9.4.1, per changes described at:
  http://www.postgresql.org/docs/9.4/static/release-9-4-1.html
- Improve .bash_profile, and let users specify their own
  environmental settings by sourcing an external file, called
  ~/.pgsql_profile. Per request from various users, and final
  suggestion from Martin Gudmundsson.

* Wed Dec 17 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4.0-1PGDG
- Update to 9.4.0

* Tue Nov 18 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4rc1-1PGDG
- Update to 9.4 rc1

* Wed Oct 8 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4beta3-1PGDG
- Update to 9.4 beta 3

* Mon Sep 01 2014 Craig Ringer <craig@2ndquadrant.com> - 9.4beta2-4PGDG
- Use libuuid from e2fsprogs instead of ossp-uuid to remove EPEL dependency
- Remove obsolete /var/log/pgsql
- Remove Provides: entry for libpq.so (RPM generates one)

* Wed Aug 27 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4beta2-3PGDG
- Fix perl requires incancation, per Craig Ringer.

* Mon Jul 28 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4beta2-2PGDG
- Fix setup script, so that it does not look for PGPORT variable. Per
  Jesper Petersen.

* Tue Jul 22 2014 Devrim Gündüz <devrim@gunduz.org> - 9.4beta2-1PGDG
- Update to 9.4 beta 2

* Thu May 15 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.4beta1-2PGDG
- Add a new script, called postgresql94-check-db-dir, to be used in
  unit file in ExecStartPre. This is a feature we used to have in
  old init scripts. Per Fedora RPMs.
- Fix permissions of postgresql-94-libs.conf, per Christoph Berg.

* Thu May 15 2014 Jeff Frost <jeff@pgexperts.com> - 9.4beta1-1PGDG
- Update to 9.4 beta 1

* Tue Mar 18 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.4-1PGDG
- Update to 9.3.4, per changes described at:
  http://www.postgresql.org/docs/9.3/static/release-9-3-4.html

* Tue Feb 18 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.3-1PGDG
- Update to 9.3.3, per changes described at:
  http://www.postgresql.org/docs/9.3/static/release-9-3-3.html

* Thu Dec 12 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.2-2PGDG
- Fix builds when uuid support is disabled, by adding missing conditional.

* Wed Dec 04 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.2-1PGDG
- Update to 9.3.2, per changes described at:
  http://www.postgresql.org/docs/9.3/static/release-9-3-2.html

* Tue Oct 8 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.1-1PGDG
- Update to 9.3.1, per changes described at:
  http://www.postgresql.org/docs/9.3/static/release-9-3-1.html

* Tue Sep 3 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3.0-1PGDG
- Update to 9.3.0

* Tue Aug 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3rc1-1PGDG
- Update to 9.3 RC1

* Sun Jun 30 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3beta2-2PGDG
- Enable building with --with-selinux by default.

* Wed Jun 26 2013 Jeff Frost <jeff@pgexperts.com> - 9.3beta2-1PGDG
- Update to 9.3 beta 2

* Sun May 12 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3beta1-2PGDG
- Set log_line_prefix in default config file to %m. Per suggestion
  from Magnus. Fixes #91.

* Tue May 07 2013 Jeff Frost <jeff@pgexperts.com> - 9.3beta1-1PGDG
- Initial cut for 9.3 beta 1

* Wed Apr 17 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.4-3PGDG
- Fix Requires: for pltcl package. Per report from Peter Dean.
  Fixes #101.

* Thu Apr 11 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.4-2PGDG
- Add pg_basebackup to $PATH, per #75.

* Tue Apr 02 2013 Jeff Frost <jeff@pgexperts.com> - 9.2.4-1PGDG
- Update to 9.2.4, per changes described at:
  http://www.postgresql.org/docs/9.2/static/release-9-2-4.html
  which also includes fixes for CVE-2013-1899, CVE-2013-1900, and
  CVE-2013-1901.

* Fri Feb 8 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.3-2PGDG
- Fix bug in new installations, that prevents ld.so.conf.d file
  to be installed.

* Wed Feb 6 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.3-1PGDG
- Update to 9.2.3, per changes described at:
  http://www.postgresql.org/docs/9.2/static/release-9-2-3.html
- Fix -libs issue while installing 9.1+ in parallel. Per various
  bug reports. Install ld.so.conf.d file with -libs subpackage.
- Move $pidfile and $lockfile definitions before sysconfig call,
  so that they can be included in sysconfig file.

* Thu Dec 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.2-1PGDG
- Update to 9.2.2, per changes described at:
  http://www.postgresql.org/docs/9.2/static/release-9-2-2.html

* Thu Sep 20 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.1-1PGDG
- Update to 9.2.1, per changes described at:
  http://www.postgresql.org/docs/9.2/static/release-9-2-1.html
- Initial cut for pg_upgrade support on PGDG RPMs.
  Usage: postgresql92-setup upgrade

* Thu Sep 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2.0-1PGDG
- Update to 9.2.0
- Split .control files in appropriate packages. This is a late port
  from 9.1 branch. With this patch, pls can be created w/o installing
  -contrib subpackage.

* Tue Aug 28 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2rc1-2
- Install linker conf file with alternatives, so that the latest
  version will always be used. Fixes #77.

* Fri Aug 24 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2rc1-1
- Update to 9.2 RC1

* Thu Aug 16 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2beta4-1
- Update to 9.2 beta4, which also includes fixes for CVE-2012-3489
  and CVE-2012-3488.

* Mon Aug 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2beta3-1
- Update to 9.2 beta3

* Wed Jun 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2beta2-1
- Update to 9.2 beta2, which also includes fixes for CVE-2012-2143,
  CVE-2012-2655.

* Fri May 11 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2-beta1-1PGDG
- Initial cut for 9.2 beta 1

* Fri Feb 24 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.3-1PGDG
- Update to 9.1.3, per the changes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-3.html
  which	also includes fixes for	CVE-2012-0866, CVE-2012-0867 and
  CVE-2012-0868	.

* Fri Dec 02 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.2-1PGDG
- Update to 9.1.2, per the changes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-2.html
- Fix nls related build issues: Enable builds when %%nls is 1, but
  %%pl* is 0.
- Change service named to postgresql-9.1.service, to make it compatible
  with previous releases.

* Wed Nov 9 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.1-4PGDG
- Use native systemd support. Patches are taken from Fedora, and
  adjusted for PGDG layout.
- Initial F-16 support.
- Improve CFLAGS
- Improve package descriptions, per Fedora spec.

* Tue Oct 18 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.1-3PGDG
- Move doc directory only once. Per Alex Tkachenko.

* Wed Oct 5 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.1-2PGDG
- Explicitly Provide: versionless postgresql*, to satisfy dependencies
  in OS packages. Already did it in -jdbc package, and it worked.

* Fri Sep 23 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.1-1PGDG
- Update to 9.1.1, per the changes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-1.html

* Mon Sep 19 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.0-3PGDG
- Add support for compilation with selinux. Patch from Daymel
  Bonne Solís.

* Mon Sep 12 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1.0-2PGDG
- Add plpgsql.control to -server subpackage, so initdb won't be broken (and we
  will not need to install -contrib subpackage)..

* Fri Sep 9 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1.0-1PGDG
- Update to 9.1.0 Gold, per
  http://www.postgresql.org/docs/9.1/static/release-9-1.html
- Update several patches, per Tom's Fedora RPMs.

* Sat Aug 20 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1rc1-1PGDG
- Update to 9.1 RC1
- Revert init script change for RHCS, since it breaks stop() routine.

* Tue Aug 9 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1beta3-1PGDG
- Update to 9.1 beta3

* Fri Jun 10 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1beta2-1PGDG
- Update to 9.1 beta2

* Mon Jun 6 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1beta1-1PGDG
- Update to 9.1 beta1

* Tue Mar 29 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1alpha5-1PGDG
- Update to 9.1 alpha5
- Add new option to init script to specify locale during initdb.

* Thu Mar 10 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1alpha4-1PGDG
- Update to 9.1 alpha4

* Fri Jan 7 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.1alpha3-1PGDG
- Port various fixes from 9.0 branch.
- Update to 9.1 alpha3
- Remove Conflicts for pre 7.4
- Trim changelog

* Wed Sep 8 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.1alpha1-1PGDG
- Initial cut for 9.1 Alpha1.
- Init script, libdir, etc. updates.
- Bump up alternatives version.
- Fix alternatives section for psql.

