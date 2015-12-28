%global postgismajorversion 2.2
%global postgisprevmajorversion 2.1
%global postgisprevversion 2.1.8
%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname	postgis
%{!?utils:%global	utils 1}
%{!?raster:%global	raster 1}

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}2_%{pgmajorversion}
Version:	2.2.0
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source1:	http://download.osgeo.org/%{sname}/source/%{sname}-%{postgisprevversion}.tar.gz
Source2:	http://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	filter-requires-perl-Pg.sh
Patch0:		postgis-2.2.0-gdalfpic.patch

URL:		http://www.postgis.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, proj-devel, geos-devel >= 3.4.2
BuildRequires:	proj-devel, flex, json-c-devel, libxml2-devel, SFCGAL-devel
%if %raster
BuildRequires:	gdal-devel
%endif

Requires:	postgresql%{pgmajorversion}, geos >= 3.4.2, proj, hdf5, json-c
Requires:	SFCGAL
Requires(post):	%{_sbindir}/update-alternatives

Provides:	%{sname} = %{version}-%{release}

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Group:		Applications/Databases
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}

%description devel
The postgis-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases

%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}

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

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
        --without-raster \
%endif
	 --disable-rpath --libdir=%{pginstdir}/lib --with-sfcgal=%{_bindir}/sfcgal-config

make LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"
make -C extensions

%if %utils
 make -C utils
%endif

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# PostGIS 2.1 breaks compatibility with 2.0, and we need to ship
# postgis-2.0.so file along with 2.1 package, so that we can upgrade:
tar zxf %{SOURCE1}
cd %{sname}-%{postgisprevversion}

%configure --with-pgconfig=%{pginstdir}/bin/pg_config --without-raster \
	 --disable-rpath --libdir=%{pginstdir}/lib

make LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgisprevmajorversion}.so"
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
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*legacy*.sql
%{pginstdir}/share/contrib/%{sname}_topology-%{postgismajorversion}/*topology*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*sfcgal*.sql
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%{pginstdir}/lib/liblwgeom*.so.*
%{pginstdir}/lib/postgis_topology-2.2.so
%{pginstdir}/lib/address_standardizer-2.2.so
%{pginstdir}/lib/liblwgeom.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%if %raster
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*rtpostgis*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/topology*.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/*

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
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
* Fri Oct 30 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-2
- Build with SFCGAL support.
- use -fPIC with gdal, patch from Oskari Saarenmaa.

* Tue Oct 13 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0, per changes described at:
  http://postgis.net/2015/10/07/postgis-2.2.0
  using 2.1.8 spec file.
- Don't use smp_flags in make, as it breaks build.
- Trim changelog.
