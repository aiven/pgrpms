%undefine _debugsource_packages
%global postgismajorversion 2.5
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.4
%global sname	postgis
%global _smp_mflags    -j1

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global	libspatialitemajorversion	43
%else
%global	libspatialitemajorversion	50
%endif

%pgdg_set_gis_variables

# Override PROJ major version on PostGIS 2.5
# Does not build against Proj >= 8.0.0
%global projmajorversion 72
%global projfullversion 7.2.1
%global projinstdir /usr/proj%{projmajorversion}

%{!?utils:%global	utils 1}
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1315
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%else
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 0}
%endif
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1315
%{!?raster:%global     raster 1}
%else
%{!?raster:%global     raster 0}
%endif
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1315
%ifnarch ppc64 ppc64le
# TODO
%{!?sfcgal:%global     sfcgal 1}
%else
%{!?sfcgal:%global     sfcgal 0}
%endif
%else
%{!?sfcgal:%global    sfcgal 0}
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.6
Release:	1%{?dist}
License:	GPLv2+
Source0:	http://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source2:	http://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch

URL:		http://www.postgis.net/


BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	pcre-devel pgdg-srpm-macros >= 1.0.10
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libjson-c-devel proj%{projmajorversion}-devel >= %{projfullversion}
%endif
%else
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion} flex json-c-devel
%endif
BuildRequires:	libxml2-devel
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
  %if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:	gdal-devel >= 1.9.2-9
  %else
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
  %endif
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
BuildRequires:	protobuf-c-devel
%endif

Requires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-contrib
Requires:	geos%{geosmajorversion} >= %{geosfullversion} proj%{projmajorversion} >= %{projfullversion}
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	pcre
%if 0%{?suse_version} >= 1315
Requires:	libjson-c2 gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
Requires:	libxerces-c-3_1
%else
Requires:	json-c xerces-c
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	gdal-libs >= 1.9.2-9
%else
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
Requires:	protobuf-c
%endif

%endif
Requires(post):	%{_sbindir}/update-alternatives

Provides:	%{sname} = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion} <= %{postgismajorversion}.2-1
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
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-client <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-client => %{postgismajorversion}.0

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-devel <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-devel => %{postgismajorversion}.0

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %{shp2pgsqlgui}
%package	gui
Summary:	GUI for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	gui
The %{name}-gui package provides a gui for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-utils <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-utils => %{postgismajorversion}.0

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0
%if 0%{?rhel} && 0%{?rhel} <= 6
%patch1 -p0
%endif

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{libspatialiteinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64";  export SFCGAL_LDFLAGS

LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff -L/usr/lib64"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib/pkgconfig

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
	--enable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/%{geosinstdir}/bin/geos-config \
	--with-gdalconfig=%{gdalinstdir}/bin/gdal-config \
	--with-projdir=%{projinstdir}

SHLIB_LINK="$SHLIB_LINK" %{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgismajorversion}.so"

%{__make} -C extensions

%if %utils
 SHLIB_LINK="$SHLIB_LINK" %{__make} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
SHLIB_LINK="$SHLIB_LINK" %{__make} install DESTDIR=%{buildroot}

%if %utils
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create symlink of .so file. PostGIS hackers said that this is safe:
%{__ln_s} %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so %{buildroot}%{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so
%{__ln_s} %{pginstdir}/lib/%{sname}_topology-%{postgismajorversion}.so %{buildroot}%{pginstdir}/lib/%{sname}_topology-%{postgisprevmajorversion}.so
%if %{raster}
%{__ln_s} %{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so %{buildroot}%{pginstdir}/lib/rtpostgis-%{postgisprevmajorversion}.so
%endif

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
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.TXT
%else
%license LICENSE.TXT
%endif
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_for_extension.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*topology*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_proc_set_search_path.sql
%if %{sfcgal}
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*sfcgal*.sql
%endif
%{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%if %{sfcgal}
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/liblwgeom*.so.*
%{pginstdir}/lib/%{sname}_topology-%{postgismajorversion}.so
%{pginstdir}/lib/%{sname}_topology-%{postgisprevmajorversion}.so
%{pginstdir}/lib/address_standardizer.so
%{pginstdir}/lib/liblwgeom.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_comments.sql
%if %{raster}
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*rtpostgis*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%{pginstdir}/lib/rtpostgis-%{postgisprevmajorversion}.so
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%endif
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/address_standardizer*.bc
   %{pginstdir}/lib/bitcode/address_standardizer/*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgismajorversion}/*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgismajorversion}/*.bc
   %if %raster
   %{pginstdir}/lib/bitcode/rtpostgis-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/rtpostgis-%{postgismajorversion}/*.bc
   %endif
  %endif
 %endif
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
%{pginstdir}/lib/liblwgeom*.a
%{pginstdir}/lib/liblwgeom*.la

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%if %shp2pgsqlgui
%files gui
%defattr(-,root,root)
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%changelog
* Tue Apr 26 2022 Devrim Gündüz <devrim@gunduz.org> 2.5.6-1
- Update to 2.5.6

* Wed Jul 14 2021 Devrim Gunduz <devrim@gunduz.org> - 2.5.5-5
- Merge some flags from 3.x spec files.

* Mon Mar 22 2021 Devrim Gunduz <devrim@gunduz.org> - 2.5.5-4
- Rebuild against GeOS 3.9.1
- Override PROJ major version. PostGIS 2.5 does not build against
  Proj 8.0.0

* Tue Dec 22 2020 Devrim Gunduz <devrim@gunduz.org> - 2.5.5-3
- Rebuild against GeOS 3.9.0

* Tue Nov 10 2020 Devrim Gunduz <devrim@gunduz.org> - 2.5.5-2
- Rebuild against new GDAL 3.2.0 and PROJ 7.2.0

* Mon Aug 17 2020 Devrim Gündüz <devrim@gunduz.org> 2.5.5-1
- Update to 2.5.5

* Tue May 5 2020 Devrim Gündüz <devrim@gunduz.org> 2.5.4-2
- Rebuild against Proj 7.0.1

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> 2.5.4-1
- Update to 2.5.4
- Build with Proj 7.0.0, and GeOS 3.8.1

* Wed Feb 26 2020 Devrim Gündüz <devrim@gunduz.org> 2.5.3-8
- Rebuild for Proj 6.3.1

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> 2.5.3-7
- Rebuild for Proj 6.3.0 and GDAL 3.0.4

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> 2.5.3-6
- Rebuild for GEOS 3.8.0, Proj 6.2.1 and GDAL 3.0.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-5.1
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 2.5.3-5
- Rebuild for GeOS 3.7.2

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-4
- Sync with 3.0 spec file
- Update GDAL dependency to 3.0.1
- Update Proj to 6.2

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-3
- Add xerces-c dependency, per https://redmine.postgresql.org/issues/4672

* Fri Aug 23 2019 John K. Harvey <john.harvey@crunchydata.com> - 2.5.3-2
- Update to 2.5.3-2, which allows protocol buffer support in EL-7

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-1
- Update to 2.5.3

* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-5
- Add protobuf dependency only for RHEL 8 and Fedora, per
  https://redmine.postgresql.org/issues/4390#note-3

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-4
- Add protobuf-c dependency, so that related functions can be used.
  Per https://redmine.postgresql.org/issues/4390

* Fri Jun 7 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-3
- Fix build-id conflict. Per report from Laurenz Albe:
  https://www.postgresql.org/message-id/33eb80b3f74b332d5eeee95825f91e45858ecd90.camel%40cybertec.at
- Link to our GeOS.

* Wed Jun 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-2
- Fix Fedora builds (CLANG)
- Use new gdal23 package as dependency.

* Fri Mar 15 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1
- Update to 2.5.2

* Tue Jan 29 2019 John K. Harvey <john.harvey@crunchydata.com> - 2.5.1-5
- Support builds on EL-6
- Break out postgis-gui components into their own sub-package

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-4
- Enable rpath builds to embed the right GeOS and Proj version to
  PostGIS libraries.

* Sun Dec 30 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-3
- Also add a symlink for postgis_topology, per Paul.

* Thu Nov 29 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-2
- Attempt to fix pg_upgrade issues on RHEL 7.

* Thu Nov 29 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
* Fix RHEL 7 issues. Patch from John Harvey.
- Update to 2.5.1

* Wed Oct 24 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-2
- Depend on GeOS 3.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Sep 24 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0 Gold

* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0beta2-1
- Initial cut for PostGIS 2.5.0 beta2
