%global pgmajorversion 91
%global	pginstdir /usr/pgsql-9.1
%global debug_package %{nil}

Name:		postgresql%{pgmajorversion}-odbc
Summary:	PostgreSQL ODBC driver
Version:	09.05.0400
Release:	1PGDG%{?dist}
License:	LGPLv2
Group:		Applications/Databases
URL:		https://odbc.postgresql.org/

Source0:	http://download.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz
Source1:	acinclude.m4

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	unixODBC-devel
BuildRequires:	libtool automake autoconf postgresql%{pgmajorversion}-devel
BuildRequires:	openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:	postgresql%{pgmajorversion}-libs
Provides:	postgresql-odbc

# This spec file and ancillary files are licensed in accordance with
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n psqlodbc-%{version}

# Some missing macros.  Courtesy Owen Taylor <otaylor@redhat.com>.
%{__cp} -p %{SOURCE1} .
# Use build system's libtool.m4, not the one in the package.
%{__rm} -f libtool.m4

libtoolize --force  --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build

./configure --with-unixodbc --with-libpq=%{pginstdir} -disable-dependency-tracking --libdir=%{_libdir}

make

%install
%{__rm} -rf %{buildroot}
%makeinstall

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file

install -d -m 755 %{buildroot}%{pginstdir}/lib
pushd %{buildroot}%{pginstdir}/lib
	ln -s psqlodbcw.so psqlodbc.so
	mv %{buildroot}%{_libdir}/psqlodbc*.so %{buildroot}%{pginstdir}/lib
	rm %{buildroot}%{_libdir}/psqlodbcw.la
popd
strip %{buildroot}%{pginstdir}/lib/*.so

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{pginstdir}/lib/psqlodbcw.so
%{pginstdir}/lib/psqlodbc.so
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc license.txt readme.txt
%else
%doc readme.txt
%license license.txt
%endif


%changelog
* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0400-1
- Update to 09.05.0400
- Remove ancient comments from the header of the spec file.

* Mon Apr 18 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0200-1
- Update to 09.05.0200

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0100-1
- Update to 09.05.0100
- Update download URL
- Use a few more macros in spec file.

* Sun Apr 5 2015 - Devrim GUNDUZ <devrim@gunduz.org> - 09.03.0400-1
- Update to 09.03.0400
- Provide postgresql-odbc package (versionless)
- Update URL

* Mon May 19 2014 - Devrim GUNDUZ <devrim@gunduz.org> - 09.03.0300-1
- Update to 09.03.0300

* Fri Dec 20 2013 - Devrim GUNDUZ <devrim@gunduz.org> - 09.03.0100-1
- Update to 09.03.0100

* Sat Nov 9 2013 - Devrim GUNDUZ <devrim@gunduz.org> - 09.02.0100-1
- Update to 09.02.0100

* Sat Nov 9 2013 - Devrim GUNDUZ <devrim@gunduz.org> - 09.02.0200
- Update to 09.02.0200

* Mon Sep 10 2012 - Devrim GUNDUZ <devrim@gunduz.org> - 09.01.0200
- Update to 09.01.0200

* Tue Nov 8 2011 - Devrim GUNDUZ <devrim@gunduz.org> - 09.00.0310
- Update to 09.00.0310.

* Tue Nov 9 2010 - Devrim GUNDUZ <devrim@gunduz.org> - 09.00.0200
- Update to 09.00.0200, and also apply changes for new RPM layout.

* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 08.04.0200-1PGDG
- Update to 08.04.0200
- Use new parameter --with-libpq in order to support multiple version
  installation of PostgreSQL.
- Remove --with-odbcinst parameter.
- Add new global variable to support multiple version installation
  of PostgreSQL.
- Update URL.
- Update license
- Add new BRs, per Fedora spec.
- Use build system's libtool.m4, not the one in the package.
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.
- Add -disable-dependency-tracking, per Fedora spec.
- Trim changelog (see svn repo for history)
