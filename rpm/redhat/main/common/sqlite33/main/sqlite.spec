%global sname	sqlite
%global sqlite33instdir /usr/sqlite330

%define	realver	3300100
%define	docver	3300100
%define	rpmver	3.30.1

Summary:	Library that implements an embeddable SQL database engine
Name:		%{sname}33
Version:	%{rpmver}
Release:	7%{?dist}.1
License:	Public Domain
URL:		https://www.sqlite.org/

Source0:	http://www.sqlite.org/2019/sqlite-src-%{realver}.zip
Source1:	http://www.sqlite.org/2019/sqlite-doc-%{docver}.zip
Source2:	http://www.sqlite.org/2019/sqlite-autoconf-%{realver}.tar.gz
# Support a system-wide lemon template
Patch1:		sqlite-3.6.23-lemon-system-template.patch
# sqlite >= 3.7.10 is buggy if malloc_usable_size() is detected, disable it:
# https://bugzilla.redhat.com/show_bug.cgi?id=801981
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=665363
Patch2:		sqlite-3.12.2-no-malloc-usable-size.patch
# Temporary workaround for failed percentile test, see patch for details
Patch3:		sqlite-3.8.0-percentile-test.patch
# Disable test date-2.2c on i686
Patch4:		sqlite-3.16-datetest-2.2c.patch
# Modify sync2.test to pass with DIRSYNC turned off
Patch5:		sqlite-3.18.0-sync2-dirsync.patch
# Enable ppc64le support in configure
Patch6:		sqlite33-configure-ppc64le.patch

BuildRequires:	gcc
BuildRequires:	ncurses-devel readline-devel glibc-devel
BuildRequires:	autoconf pgdg-srpm-macros

Requires:		%{name}-libs = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes:		%{name} < 3.11.0-1
Conflicts:		%{name} < 3.11.0-1

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary:	Development tools for the sqlite3 embeddable SQL database engine
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%package libs
Summary:	Shared library for the sqlite3 embeddable SQL database engine.

# Ensure updates from pre-split work on multi-lib systems
Obsoletes:	%{name} < 3.11.0-1
Conflicts:	%{name} < 3.11.0-1

%description libs
This package contains the shared library for %{name}.

%package doc
Summary:	Documentation for sqlite
BuildArch: noarch

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package -n %{name}-lemon
Summary:	A parser generator

%description -n %{name}-lemon
Lemon is an LALR(1) parser generator for C or C++. It does the same
job as bison and yacc. But lemon is not another bison or yacc
clone. It uses a different grammar syntax which is designed to reduce
the number of coding errors. Lemon also uses a more sophisticated
parsing engine that is faster than yacc and bison and which is both
reentrant and thread-safe. Furthermore, Lemon implements features
that can be used to eliminate resource leaks, making is suitable for
use in long-running programs such as graphical user interfaces or
embedded controllers.

%prep
%setup -q -a1 -n sqlite-src-%{realver}
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p0

# Remove backup-file
%{__rm} -f %{sname}-doc-%{docver}/sqlite.css~ || :

autoconf # Rerun with new autoconf to add support for aarm64

%build
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 \
		-DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 \
		-DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 \
		-DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
		-DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -DSQLITE_ENABLE_JSON1=1 \
		-DSQLITE=THREADSAFE=2 -Wall -fno-strict-aliasing"

./configure --disable-tcl \
	--prefix=%{sqlite33instdir} \
	--libdir=%{sqlite33instdir}/lib \
	--enable-fts5 \
	--enable-threadsafe \
	--enable-threads-override-locks \
	--enable-load-extension

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{sqlite33instdir}/man/man1/sqlite3.1
%{__install} -D -m0755 lemon $RPM_BUILD_ROOT/%{sqlite33instdir}/bin/lemon
%{__install} -D -m0644 tool/lempar.c $RPM_BUILD_ROOT/%{sqlite33instdir}/data/lemon/lempar.c

%if ! %{with static}
%{__rm} -f $RPM_BUILD_ROOT/%{sqlite33instdir}/lib/*.{la,a}
%endif
# Create linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{sqlite33instdir}/lib/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf


%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%{sqlite33instdir}/bin/sqlite3
%{sqlite33instdir}/man/man?/*

%files libs
%doc README.md
%{sqlite33instdir}/lib/*.so.*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%{sqlite33instdir}/include/*.h
%{sqlite33instdir}/lib/*.so
%{sqlite33instdir}/lib/pkgconfig/*.pc
%if %{with static}
%{sqlite33instdir}/lib/*.a
%exclude %{sqlite33instdir}/lib/*.la
%endif

%files doc
%doc %{sname}-doc-%{docver}/*

%files -n %{name}-lemon
%{sqlite33instdir}/bin/lemon
%{sqlite33instdir}/data/lemon

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.30.1-7.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-7
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Fri Apr 9 2021 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-6
- Add linker config file, per #6373

* Wed Feb 17 2021 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-5
- Add full multithreading support, per
  https://redmine.postgresql.org/issues/5189

* Wed May 6 2020 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-4
- Add ppc64le support. Patch from Talha Bin Rizwan

* Thu Mar 19 2020 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-3
- Fix ldconfig path (for SLES 12)
- Fix an rpmlint warning

* Sat Feb 15 2020 Devrim Gündüz <devrim@gunduz.org> - 3.30-1-2
- Remove tcl and  analyze subpackages. We don't need them.

* Wed Nov 13 2019 Devrim Gündüz <devrim@gunduz.org> - 3.30-1.1
- Initial packaging for PostgreSQL RPM repository to fix
  performance issues on RHEL 7 with new Proj and co.
