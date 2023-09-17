Name:		postgresql%{pgmajorversion}-odbc
Summary:	PostgreSQL ODBC driver
Version:	16.00.0000
Release:	1PGDG%{?dist}
License:	LGPLv2
URL:		https://odbc.postgresql.org/

Source0:	https://download.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz
Source1:	acinclude.m4

BuildRequires:	unixODBC-devel pgdg-srpm-macros
BuildRequires:	libtool automake autoconf postgresql%{pgmajorversion}-devel
BuildRequires:	openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:	postgresql%{pgmajorversion}-libs
Provides:	postgresql-odbc%{?_isa} >= 08.00.0100

# This spec file and ancillary files are licensed in accordance with
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n psqlodbc-%{version}
%ifarch ppc64le
sed -i "s:elf64ppc:elf64lppc:g" configure
%endif

# Some missing macros. Courtesy Owen Taylor <otaylor@redhat.com>.
%{__cp} -p %{SOURCE1} .
# Use build system's libtool.m4, not the one in the package.
%{__rm} -f libtool.m4

libtoolize --force --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build
chmod +x configure
	./configure --with-unixodbc --with-libpq=%{pginstdir} -disable-dependency-tracking --libdir=%{_libdir}
%{__make}

%install
%{__rm} -rf %{buildroot}
%makeinstall

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file

%{__install} -d -m 755 %{buildroot}%{pginstdir}/lib
pushd %{buildroot}%{pginstdir}/lib
	%{__ln_s} psqlodbcw.so psqlodbc.so
	%{__mv} %{buildroot}%{_libdir}/psqlodbc*.so %{buildroot}%{pginstdir}/lib
	%{__rm} %{buildroot}%{_libdir}/psqlodbcw.la
	%{__rm} %{buildroot}%{_libdir}/psqlodbca.la
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{pginstdir}/lib/psqlodbcw.so
%{pginstdir}/lib/psqlodbc.so
%{pginstdir}/lib/psqlodbca.so
%doc readme.txt
%license license.txt

%changelog
* Sun Sep 17 2023 Devrim Gündüz <devrim@gunduz.org> - 16.00.0000-1PGDG
- Update to 16.00.0000

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 15.00.0000-2PGDG
- Remove RHEL 6 bits
- Fix rpmlint warnings

* Fri Jun 23 2023 Devrim Gündüz <devrim@gunduz.org> - 15.00.0000-1PGDG
- Update to 15.00.0000

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 13.02.0000-2PGDG
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 25 2021 Devrim Gündüz <devrim@gunduz.org> - 13.02.0000-1PGDG
- Update to 13.02.0000

* Wed May 12 2021 Devrim Gündüz <devrim@gunduz.org> - 13.01.0000-1PGDG
- Update to 13.01.0000

* Wed Dec 23 2020 Devrim Gündüz <devrim@gunduz.org> - 13.00.0000-1PGDG
- Update to 13.00.0000

* Thu May 28 2020 Devrim Gündüz <devrim@gunduz.org> - 12.02.0000-1PGDG
- Update to 12.02.0000

* Thu May 21 2020 Devrim Gündüz <devrim@gunduz.org> - 12.01.0000-2PGDG
- Add debuginfo packages, per Aqeel.

* Mon Jan 27 2020 Devrim Gündüz <devrim@gunduz.org> - 12.01.0000-1PGDG
- Update to 12.01.0000

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 12.00.0000-1PGDG
- Update to 12.00.0000

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 11.01.0000-1PGDG.1
- Rebuild for PostgreSQL 12

* Tue May 28 2019 Devrim Gündüz <devrim@gunduz.org> - 11.01.0000-1PGDG
- Update to 11.01.0000

* Tue Dec 11 2018 Devrim Gündüz <devrim@gunduz.org> - 11.00.0000-1PGDG
- Update to 11.00.0000

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 10.03.0000-1PGDG.1
- Rebuild against PostgreSQL 11.0

* Sun May 27 2018 - Devrim Gündüz <devrim@gunduz.org> - 10.03.0000-1
- Update to 10.03.0000

* Fri Mar 30 2018 - Devrim Gündüz <devrim@gunduz.org> - 10.02.0000-1
- Update to 10.02.0000

* Tue Jan 2 2018 - Devrim Gündüz <devrim@gunduz.org> - 10.01.0000-1
- Update to 10.01.0000

* Sun Oct 15 2017 - Devrim Gündüz <devrim@gunduz.org> - 10.00.0000-1
- Update to 10.00.0000

* Fri Sep 22 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0500-1
- Update to 09.06.0500

* Wed Aug 2 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0410-1
- Update to 09.06.0410

* Sun May 28 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0310-1
- Update to 09.06.0310

* Wed May 10 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0300-1
- Update to 09.06.0300

* Thu Apr 6 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0200-1
- Update to 09.06.0200

* Wed Feb 8 2017 - Devrim Gündüz <devrim@gunduz.org> - 09.06.0100-1
- Update to 09.06.0100

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0400-1
- Update to 09.05.0400
- Remove ancient comments from the header of the spec file.

* Mon Apr 18 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0200-1
- Update to 09.05.0200

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> - 09.05.0100-1
- Update to 09.05.0100
- Update download URL
- Use a few more macros in spec file.

* Sun Apr 5 2015 - Devrim Gündüz <devrim@gunduz.org> - 09.03.0400-1
- Update to 09.03.0400
- Provide postgresql-odbc package (versionless)
- Update URL

* Mon May 19 2014 - Devrim Gündüz <devrim@gunduz.org> - 09.03.0300-1
- Update to 09.03.0300

* Fri Dec 20 2013 - Devrim Gündüz <devrim@gunduz.org> - 09.03.0100-1
- Update to 09.03.0100

* Sat Nov 9 2013 - Devrim Gündüz <devrim@gunduz.org> - 09.02.0100-1
- Update to 09.02.0100

* Sat Nov 9 2013 - Devrim Gündüz <devrim@gunduz.org> - 09.02.0200
- Update to 09.02.0200

* Mon Sep 10 2012 - Devrim Gündüz <devrim@gunduz.org> - 09.01.0200
- Update to 09.01.0200

* Tue Nov 8 2011 - Devrim Gündüz <devrim@gunduz.org> - 09.00.0310
- Update to 09.00.0310.

* Tue Nov 9 2010 - Devrim Gündüz <devrim@gunduz.org> - 09.00.0200
- Update to 09.00.0200, and also apply changes for new RPM layout.

* Tue Mar 9 2010 Devrim Gündüz <devrim@gunduz.org> 08.04.0200-1PGDG
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
