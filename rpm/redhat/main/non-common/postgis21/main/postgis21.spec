%global debug_package %{nil}

%global postgismajorversion 2.1
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.0
%global postgisprevversion %{postgisprevmajorversion}.7
%global sname	postgis

%{!?utils:%global	utils 1}
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 0}
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 6
%{!?raster:%global     raster 1}
%else
%{!?raster:%global     raster 0}
%endif
# The RPM's for PostGIS 2.1 generally do not build with sfcgal on
# However, this can optionally be overrideen for fedora >= 24 or rhel >= 7
%{!?sfcgal:%global    sfcgal 0}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.9
Release:	5%{?dist}
License:	GPLv2+
Source0:	http://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source1:	http://download.osgeo.org/%{sname}/source/%{sname}-%{postgisprevversion}.tar.gz
Source2:	http://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch
# To be removed when 2.0.8 is out:
Patch1:		postgis21-2.0.7-pg95.patch

URL:		http://www.postgis.net/

BuildRequires:	pgdg-srpm-macros postgresql%{pgmajorversion}-devel
BuildRequires:	geos36-devel >= 3.6.2 pcre-devel
BuildRequires:	proj49-devel, flex, json-c-devel, libxml2-devel
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	gdal-devel >= 1.9.0
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif
%endif

Requires:	postgresql%{pgmajorversion} geos36 >= 3.6.2
Requires:	postgresql%{pgmajorversion}-contrib proj49
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	gdal-libs > 1.9.0, json-c, pcre
Requires(post):	%{_sbindir}/update-alternatives

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
%endif

Provides:	%{sname} = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion} <= %{postgismajorversion}.5-1
Provides:	%{sname}2_%{pgmajorversion} => %{postgismajorversion}.0

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
%endif
Obsoletes:	%{sname}2_%{pgmajorversion}-client <= %{postgismajorversion}.5-1
Provides:	%{sname}2_%{pgmajorversion}-client => %{postgismajorversion}.0

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-devel <= %{postgismajorversion}.5-1
Provides:	%{sname}2_%{pgmajorversion}-devel => %{postgismajorversion}.0
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
%endif

%description devel
The postgis-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.5-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
%endif

%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-utils <= %{postgismajorversion}.5-1
Provides:	%{sname}2_%{pgmajorversion}-utils => %{postgismajorversion}.0
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
%endif

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0

%build

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%endif

LDFLAGS="$LDFLAGS -L/usr/geos36/lib -L/usr/proj49/lib"; export LDFLAGS

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
        --without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
%if %{shp2pgsqlgui}
	--with-gui \
%endif
	--disable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/usr/geos36/bin/geos-config \
	--with-projdir=/usr/proj49

%{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"
%{__make} -C extensions

%if %utils
 %{__make} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# PostGIS 2.1 breaks compatibility with 2.0, and we need to ship
# postgis-2.0.so file along with 2.1 package, so that we can upgrade:
tar zxf %{SOURCE1}
cd %{sname}-%{postgisprevversion}
# To be removed when 2.0.8 is out:
patch -p0 -s < %{PATCH1}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%endif

%configure --with-pgconfig=%{pginstdir}/bin/pg_config --without-raster \
	--disable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/usr/geos36/bin/geos-config \
	--with-projdir=/usr/proj49

%{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgisprevmajorversion}.so"
# Install postgis-2.0.so file manually:
%{__mkdir} -p %{buildroot}/%{pginstdir}/lib/
%{__install} -m 644 postgis/postgis-%{postgisprevmajorversion}.so %{buildroot}/%{pginstdir}/lib/postgis-%{postgisprevmajorversion}.so

# Create alternatives entries for common binaries
%post
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pgmajorversion}0

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
      	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
        %{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{pginstdir}/bin/pgsql2shp
        %{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{pginstdir}/bin/shp2pgsql
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy_*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/topology*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_topology.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_sfcgal.sql
%{pginstdir}/share/extension/postgis--*.sql
%{pginstdir}/share/extension/postgis.control
%if %{sfcgal}
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal.sql
%endif
%{pginstdir}/lib/liblwgeom*.so
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%if %raster
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/rtpostgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/rtpostgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_rtpostgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/rtpostgis_legacy.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/*

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{pginstdir}/lib/liblwgeom*.a
%{pginstdir}/lib/liblwgeom*.la

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.9-4
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1.9-3.1
- Rebuild against PostgreSQL 11.0

* Mon Feb 5 2018 John Harvey <john.harvey@crunchydata.com> - 2.1.9-3
- Let PostGIS 2.1 depend on PGDG supplied Proj49 and GeOS 36 RPMs.
  This will help users to benefit from latest GeOS and Proj.

* Wed Oct 18 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1.9-2
- Require postgresql-contrib for postgis_tiger_geocoder,
  because it requires fuzzystrmatch extension.

* Wed Sep 20 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1.9-1
- Update to 2.1.9, per changes described at:
  http://postgis.net/2017/09/19/postgis-2.1.9
  Fixes #2717.

* Wed Jun 14 2017 John Harvey <john.harvey@crunchydata.com> - 2.1.8-2
- Re-add missing patch, some reorganizaton

* Tue Jul 7 2015 Devrim Gündüz <devrim@gunduz.org> - 2.1.8-1
- Update to 2.1.8, per changes described at:
  http://postgis.net/2015/07/07/postgis-2.1.8

* Fri Apr 3 2015 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-2
- Re-enable raster support, which broke upgrades.

* Thu Apr 2 2015 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1
- Update to 2.1.7, for bug and security fixes.
- Bump up postgisprevversion to 2.0.7

* Fri Mar 27 2015 Devrim Gündüz <devrim@gunduz.org> - 2.1.6-1
- Update to 2.1.6, per changes described at:
  http://postgis.net/2015/03/20/postgis-2.1.6

* Sun Dec 21 2014 Devrim Gündüz <devrim@gunduz.org> - 2.1.5-1
- Update to 2.1.5, per changes described at:
  http://postgis.net/2014/12/18/postgis-2.1.5

* Wed Sep 17 2014 Devrim Gündüz <devrim@gunduz.org> - 2.1.4-1
- Update to 2.1.4, per changes described at:
  http://postgis.net/2014/09/10/postgis-2.1.4

* Mon May 19 2014 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1
- Update to 2.1.3, for bug and security fixes.
- Bump up postgisprevversion to 2.0.6

* Wed Apr 2 2014 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-2
- Bump up postgisprevversion to 2.0.5

* Sat Mar 29 2014 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2
- Remove patch0 -- now in upstream.

* Sat Nov 9 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1
- Add a new patch for RHEL 5, per:
  http://trac.osgeo.org/postgis/ticket/2542

* Mon Oct 7 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-3
- Install postgis-2.0.so file, by compiling it from 2.0 sources.
  Per lots of complaints to maintainers and pgsql-bugs lists.
- Let main package depend on client package. Per pgrpms #141
  and per PostgreSQL bug #8463.

* Tue Sep 10 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2
- Remove ruby bindings, per
  http://lists.osgeo.org/pipermail/postgis-devel/2013-August/023690.html
- Move extension related files under main package,
  per report from Daryl Herzmann

* Mon Sep 9 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Fri Aug 9 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.0rc2
- Update to 2.1.0rc2
- Remove patch0, it is now in upstream.

* Wed Jul 31 2013 Davlet Panech <dpanech@ubitech.com> - 2.1.0beta3-2
- Fixed "provides postgis" to avoid self-conflicts
- BuildRequires: libxml2-devel

* Sun Jun 30 2013 Devrim Gündüz <devrim@gunduz.org> - 2.1.0beta3-1
- Update to 2.1.0 beta3
- Support multiple version installation
- Split "client" tools into a separate subpackage, per
  http://wiki.pgrpms.org/ticket/108
- Bump up alternatives version.
- Add dependency for mysql-devel, since Fedora / EPEL gdal packages
  are built with MySQL support, too. (for now). This is needed for
  raster support.
- Push raster support into conditionals, so that we can use similar
  spec files for RHEL and Fedora.
- Add a patch to get rid of dependency hell from gdal. Per
  http://lists.osgeo.org/pipermail/postgis-devel/2013-June/023605.html
  and a tweet from Mike Toews.

* Thu Apr 11 2013 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-2
- Provide postgis, to satisfy OS dependencies. Per #79.

* Thu Mar 14 2013 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Dec 10 2012 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2.
- Update download URL.
- Add deps for JSON-C support.

* Wed Nov 07 2012 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-2
- Add dependency to hdf5, per report from Guillaume Smet.

* Wed Jul 4 2012 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.1, for changes described at:
  http://postgis.org/news/20120622/

* Tue Apr 3 2012 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Initial packaging with PostGIS 2.0.0.
- Drop java bits from spec file.

