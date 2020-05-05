%undefine _debugsource_packages
%global postgismajorversion 2.4
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.3
%global sname	postgis

%global	geosversion	38
%global	gdalversion	30
%global	projversion	70

%pgdg_set_gis_versions

%global	geosinstdir	/usr/geos%{geosversion}
%global	projinstdir	/usr/proj%{projversion}
%global	gdalinstdir	/usr/gdal%{gdalversion}

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
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1315
%ifnarch ppc64 ppc64le
%{!?sfcgal:%global     sfcgal 1}
%else
%{!?sfcgal:%global     sfcgal 0}
%endif
%else
%{!?sfcgal:%global    sfcgal 0}
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.8
Release:	10%{?dist}
License:	GPLv2+
Source0:	http://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source2:	http://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch

URL:		http://www.postgis.net/

BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosversion}-devel >= %{geosfullversion}
BuildRequires:	pcre-devel pgdg-srpm-macros

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libjson-c-devel proj%{projversion}-devel >= %{projfullversion}
%endif
%else
BuildRequires:	proj%{projversion}-devel >= %{projfullversion} flex json-c-devel
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
BuildRequires:	gdal%{gdalversion}-devel >= %{gdalminorversion}
  %endif
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
BuildRequires:	protobuf-c-devel
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	postgresql%{pgmajorversion} geos%{geosversion} >= %{geosfullversion}
Requires:	postgresql%{pgmajorversion}-contrib proj%{projversion} >= %{projfullversion}
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	pcre
%if 0%{?suse_version} >= 1315
Requires:	libjson-c2 gdal%{gdalversion}-libs >= %{gdalminorversion}
Requires:	libxerces-c-3_1
%else
Requires:	json-c xerces-c
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	gdal-libs >= 1.9.2-9
%else
Requires:	gdal%{gdalversion}-libs >= %{gdalminorversion}
%endif
%endif
Requires(post):	%{_sbindir}/update-alternatives

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
Requires:	protobuf-c
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

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
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
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
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

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
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib" ; export SHLIB_LINK
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib -L%{gdalinstdir}/lib"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS

CFLAGS="${CFLAGS:-%optflags}"

%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

# Strip out fstack-clash-protection from CFLAGS:
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v fstack-clash-protection|xargs -n 100`; export CFLAGS
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib64"; export LDFLAGS

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

SHLIB_LINK="$SHLIB_LINK" %{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgissomajorversion}.so"
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
%if %raster
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
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/address_standardizer*.bc
   %{pginstdir}/lib/bitcode/address_standardizer/*.bc
   %{pginstdir}/lib/bitcode/%{sname}_topology-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/%{sname}_topology-%{postgismajorversion}/*.bc
   %{pginstdir}/lib/bitcode/rt%{sname}-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/rt%{sname}-%{postgismajorversion}/*.bc
  %endif
 %endif
%endif
%endif
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/%{sname}-%{postgismajorversion}/*.bc
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
* Tue May 5 2020 Devrim Gündüz <devrim@gunduz.org> 2.4.8-10
- Rebuild for Proj 7.0.1

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> 2.4.8-9
- Rebuild for Proj 7.0.0 and GeOS 3.8.1

* Wed Feb 26 2020 Devrim Gündüz <devrim@gunduz.org> 2.4.8-8
- Rebuild for Proj 6.3.1

* Wed Feb 5 2020 Devrim Gunduz <devrim@gunduz.org> - 2.4.8-7
- Proj 6.3.0 and GDAL 3.0.4

* Mon Nov 4 2019 Devrim Gunduz <devrim@gunduz.org> - 2.4.8-6
- Rebuild for GEOS 3.8.0, Proj 6.2.1 and GDAL 3.0.2

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 2.4.8-5
- Rebuild for GeOS 3.7.2

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.8-4
- Sync with 3.0 spec file
- Update GDAL dependency to 3.0.1
- Update Proj to 6.2

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.8-3
- Add xerces-c dependency, per https://redmine.postgresql.org/issues/4672

* Fri Aug 23 2019 John K. Harvey <john.harvey@crunchydata.com> - 2.4.8-2
- Update to 2.4.8-2, which allows protocol buffer support in EL-7

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.8-1
- Update to 2.4.8

* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.7-5
- Add protobuf dependency only for RHEL 8 and Fedora, per
  https://redmine.postgresql.org/issues/4390#note-3

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.7-4
- Add protobuf-c dependency, so that related functions can be used.
  Per https://redmine.postgresql.org/issues/4390

* Fri Jun 7 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.7-3
- Fix build-id conflict. Per report from Laurenz Albe:
  https://www.postgresql.org/message-id/33eb80b3f74b332d5eeee95825f91e45858ecd90.camel%40cybertec.at
- Link to our GeOS.

* Wed Jun 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.7-2
- Fix Fedora builds (CLANG)
- Use new gdal23 package as dependency.

* Fri Mar 15 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.7-1
- Update to 2.4.7

* Wed Feb 6 2019 John K. Harvey <john.harvey@crunchydata.com> - 2.4.6-4
- Break out postgis-gui components into their own sub-package
- gdal dependencies a little more verbose

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.6-3
- Enable rpath builds to embed the right GeOS and Proj version to
  PostGIS libraries.
- Also add a symlink for postgis_topology, per Paul.
- Attempt to fix pg_upgrade issues on RHEL 7.

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.6-2
- Update GeOS dependency to 3.7.

* Mon Nov 26 2018 John K. Harvey <john.harvey@crunchydata.com> - 2.4.6-1
- Update to 2.4.6
- Remove patchfile needed for 2.4.5 for clang support, since fixed in 2.4.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Tue Sep 18 2018 John K. Harvey <john.harvey@crunchydata.com> - 2.4.5-1
- Update to 2.4.5
- Includes patchfile to support 2.4.5 working with clang on PG11 for EL-7

* Thu May 3 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-2
- Remove 2.3 bits from the package, and use symlink to .so file
  instead.

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-1
- Update to 2.4.4

* Thu Jan 18 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.3-1
- Update to 2.4.3, per #3022.
- Update previous PostGIS version to 2.3.6.

* Mon Dec 25 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-5
- Rebuilt

* Tue Dec 19 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-4
- Rebuilt

* Thu Nov 23 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-3
- Make sure that we link against our GeOS and Proj packages.

* Wed Nov 22 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-2
- Let PostGIS depend on PGDG supplied Proj49 and GeOS 36 RPMs.
  This will help users to benefit from latest GeOS and Proj.

* Thu Nov 16 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2, per #2874.
- Update previous PostGIS version to 2.3.5.

* Sat Oct 21 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1, per #2819.
- Re-add 2.3 .so file for easier upgrades (2.3 can be compiled
  against PostgreSQL 10 as of 2.3.4)

* Wed Oct 18 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2
- Require postgresql-contrib for postgis_tiger_geocoder,
  because it requires fuzzystrmatch extension.

* Fri Sep 29 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0

* Wed Sep 27 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0rc3-1
- Initial packaging for 2.4

* Sun Jul 2 2017 Devrim Gündüz <devrim@gunduz.org> - 2.3.3-1
- Update to 2.3.3, per #2525 .

* Sun May 28 2017 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-2
- Rename package so that it also includes the Postgis major version.

* Mon Nov 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-1
- Update to 2.3.2, per changes described at
  http://postgis.net/2017/01/31/postgis-2.3.2
- Update previous PostGIS version to 2.2.5, per changes described at
  http://postgis.net/2017/01/30/postgis-2.2.5

* Mon Nov 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1, per changes described at
  http://postgis.net/2016/11/28/postgis-2.3.1/
- Update previous PostGIS version to 2.2.4

* Thu Oct 6 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3
- Update previous PostGIS version to 2.2.3
- Update comments about the previous version to point to the
  new releases.

* Sat Oct 01 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-2
- Rebuilt for new gdal

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0, per changes described at
  http://postgis.net/2016/09/26/postgis-2.3.0/
- Remove wildcard in -client subpackage, per John. Fixes #1769.

* Fri Mar 25 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2, per changes described at
  http://postgis.net/2016/03/22/postgis-2.2.2
- Do not attempt to install some files twice.
- Support --with-gui configure option. Patch from John Harvey,
  per #1036.

* Mon Feb 22 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3
- Fix GeOS version number in Requires part, so that it *also*
  requires GeOS >= 3.5.0. Per #1007.
- Add dependency for pcre, per #1007.

* Mon Jan 18 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3
- Force dependency on GeOS 3.5.0. Per report from Paul Edwards,
  and others, on PostGIS mailing list.

* Mon Jan 11 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2
- Fix utils, and raster macros, to fix builds on RHEL 6.
- Add macro for sfcgal support.

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1, per changes described at:
  http://postgis.net/2016/01/06/postgis-2.2.1/
- Use %%license macro, on supported distros.
- Put sfcgal and raster support into conditionals, so that
  we can use one spec file for all platforms.

* Fri Oct 30 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-2
- Build with SFCGAL support.
- use -fPIC with gdal, patch from Oskari Saarenmaa.

* Tue Oct 13 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0, per changes described at:
  http://postgis.net/2015/10/07/postgis-2.2.0
  using 2.1.8 spec file.
- Don't use smp_flags in make, as it breaks build.
- Trim changelog.
