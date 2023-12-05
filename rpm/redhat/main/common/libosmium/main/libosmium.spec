%global gdalcpp_version 1.3.0
%global protozero_version 1.6.3

%global testcommit ecfdeb0d5ffcfcb60939651d517d5d7d1bb041a3

%define debug_package %{nil}
%pgdg_set_gis_variables

# Override some variables:

%global geosfullversion %geos312fullversion
%global geosmajorversion %geos312majorversion
%global geosinstdir %geos312instdir
%global gdalfullversion %gdal36fullversion
%global gdalmajorversion %gdal36majorversion
%global gdalinstdir %gdal36instdir

Name:		libosmium
Version:	2.20.0
Release:	42PGDG%{?dist}
Summary:	Fast and flexible C++ library for working with OpenStreetMap data

License:	BSL-1.0
URL:		http://osmcode.org/%{name}/
Source0:	https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/osmcode/osm-testdata/archive/%{testcommit}/osm-testdata-%{testcommit}.tar.gz

BuildRequires:	cmake make gcc-c++
BuildRequires:	doxygen graphviz xmlstarlet
BuildRequires:	ruby rubygems spatialite-tools

BuildRequires:	catch2-devel boost-devel lz4-devel
BuildRequires:	protozero-devel >= %{protozero_version}
BuildRequires:	gdalcpp-devel >= %{gdalcpp_version}
BuildRequires:	expat-devel zlib-devel bzip2-devel sparsehash-devel
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}

BuildRequires:	catch2-static protozero-static gdalcpp-static

%description
A fast and flexible C++ library for working with OpenStreetMap data.

%package	devel
Summary:	Development files for %{name}
Provides:	%{name}-static = %{version}-%{release}

Requires:	boost-devel expat-devel zlib-devel bzip2-devel
Requires:	protozero-devel >= %{protozero_version}
Requires:	gdalcpp-devel >= %{gdalcpp_version}
Requires:	lz4-devel sparsehash-devel
Requires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
Requires:	geos%{geosmajorversion}-devel >= %{geosfullversion}

%description	devel
This package contains libraries and header files for developing
applications that use %{name}.

%package	doc
Summary:	Documentation for %{name}
BuildArch:	noarch

%description	doc
This package contains documentation for developing
applications that use %{name}.

%prep
%setup -q -c -T -a 0 -a 1
%{__mv} %{name}-%{version} %{name}
%{__mv} osm-testdata-%{testcommit} osm-testdata
%{__rm} -rf libosmium/include/gdalcpp.h libosmium/test/catch
%{__ln_s} -f /usr/include/catch2 libosmium/test/catch
sed -i -e 's/-O3 -g//' libosmium/CMakeLists.txt

%build
cd libosmium
%{__rm} include/osmium/geom/projection.hpp
%cmake -DBUILD_HEADERS=ON -DBUILD_DATA_TESTS=ON \
	-DGDAL_LIBRARY=%{gdalinstdir}/lib/libgdal.so -DGDAL_INCLUDE_DIR=%{gdalinstdir}/include \
	-DGEOS_LIBRARY=%{geosinstdir}/lib64/libgeos.so -DGEOS_INCLUDE_DIR=%{geosinstdir}/include

%cmake_build
%cmake_build --target doc

%install
cd libosmium
%cmake_install
%{__rm} -rf %{buildroot}%{_docdir}

%files devel
%doc %{name}/README.md %{name}/CHANGELOG.md
%license %{name}/LICENSE
%{_includedir}/osmium

%files doc
%doc libosmium/%{__cmake_builddir}/doc/html/*
%license libosmium/LICENSE

%changelog
* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support osm2pgsql
  package.