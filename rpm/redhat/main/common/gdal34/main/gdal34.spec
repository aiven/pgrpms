%global sname gdal

%pgdg_set_gis_variables

%global geosfullversion %geos310fullversion
%global geosmajorversion %geos310majorversion
%global geosinstdir %geos310instdir
%global projmajorversion %proj82majorversion
%global projfullversion %proj82fullversion
%global projinstdir %proj82instdir


%global gdalinstdir /usr/%{name}
%global	gdalsomajorversion	30

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global libspatialitemajorversion	43
%else
%global libspatialitemajorversion	50
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%global sqlitepname	sqlite33
%global sqlitelibdir	/usr/sqlite330/lib
# Major digit of the proj so version
%global proj_somaj 19
%else
%global sqlitepname	sqlite
%global sqlitelibdir	%{_libdir}
# Major digit of the proj so version
%global proj_somaj 22
%endif

# Override PROJ major version on RHEL 7.
# libspatialite 4.3 does not build against 8.0.0 as of March 2021.
%if 0%{?rhel} && 0%{?rhel} == 7
%global projmajorversion 72
%global projfullversion 7.2.1
%global projinstdir /usr/proj%{projmajorversion}
%endif

%if 0%{?fedora} >= 36 || 0%{?rhel} >= 7 || 0%{?suse_version} <= 1499
%global g2clib_enabled 1
%else
%global g2clib_enabled 0
%endif

#TODO: g2clib and grib (said to be modified)
#TODO: Create script to make clean tarball
#TODO: msg needs to have PublicDecompWT.zip from EUMETSAT, which is not free;
#      Building without msg therefore
#TODO: e00compr bundled?
#TODO: There are tests for bindings -- at least for Perl
#TODO: Java has a directory with test data and a build target called test
#      It uses %%{JAVA_RUN}; make test seems to work in the build directory
#TODO: e00compr source is the same in the package and bundled in GDAL
#TODO: Consider doxy patch from Suse, setting EXTRACT_LOCAL_CLASSES  = NO

# Soname should be bumped on API/ABI break
# http://trac.osgeo.org/gdal/ticket/4543

# Conditionals and structures for EL 5 are there
# to make life easier for downstream ELGIS.
# Sadly noarch doesn't work in EL 5, see
# http://fedoraproject.org/wiki/EPEL/GuidelinesAndPolicies

# He also suggest to use --with-static-proj4 to actually link to proj, instead of dlopen()ing it.


# Enable/disable generating refmans
# texlive currently broken deps and FTBFS in rawhide
%global build_refman 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492
%global mysql --with-mysql
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492
%global poppler --with-poppler
%global spatialite "--with-spatialite=%{libspatialiteinstdir}"

Name:		%{sname}34
Version:	3.4.3
Release:	8%{?dist}.1
Summary:	GIS file format library
License:	MIT
URL:		http://www.gdal.org
# Source0:	http://download.osgeo.org/gdal/%%{version}/gdal-%%{version}.tar.xz
# See PROVENANCE.TXT-fedora and the cleaner script for details!

Source0:	%{sname}-%{version}-fedora.tar.xz

# Cleaner script for the tarball
Source1:	%{sname}-cleaner.sh

Source2:	PROVENANCE.TXT-fedora
Source3:	%{name}-pgdg-libs.conf

%if 0%{?suse_version} >= 1315
Patch8:		%{sname}-3.2.1-java-sles.patch
%else
# Fedora uses Alternatives for Java
Patch8:		%{sname}-3.1.2-java.patch
%endif

# PGDG patches
Patch12:	%{name}-gdalconfig-pgdg-path.patch
Patch13:	%{name}-configure-ogdi%{ogdimajorversion}.patch

Patch16:	gdal-3.3.1-sfcgal-linker.patch

# To be removed in next update (hopefully:
BuildRequires:	autoconf

# lz4 dependency
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4
%endif

BuildRequires:	gcc gcc-c++ pgdg-srpm-macros >= 1.0.23
BuildRequires:	ant
BuildRequires:	armadillo-devel
BuildRequires:	cfitsio-devel
BuildRequires:	chrpath
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	fontconfig-devel
BuildRequires:	freexl-devel
%if 0%{?g2clib_enabled}
BuildRequires:	g2clib-devel
%endif
BuildRequires:	geos%{geosmajorversion}-devel >= 3.9.0
BuildRequires:	ghostscript
BuildRequires:	jpackage-utils
# For 'mvn_artifact' and 'mvn_install'
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%if 0%{?fedora}
BuildRequires:	libkml-devel
%endif
BuildRequires:	libspatialite%{libspatialitemajorversion}-devel

BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel
BuildRequires:	libtool
BuildRequires:	giflib-devel
BuildRequires:	netcdf-devel
%if 0%{?rhel}
BuildRequires:	mariadb-devel
%endif
%if 0%{?fedora}
BuildRequires:	mariadb-connector-c-devel
%endif
BuildRequires:	libpq5-devel
BuildRequires:	pcre2-devel
BuildRequires:	ogdi%{ogdimajorversion}-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	%{_bindir}/pkg-config
%if 0%{?suse_version} >= 1500
BuildRequires:	libpoppler-devel
%else
BuildRequires:	poppler-devel
%endif
BuildRequires:	proj%{projmajorversion}-devel >= 7.1.0
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	%{sqlitepname}-devel
%else
BuildRequires:	sqlite-devel
%endif
BuildRequires:	swig
%if %{build_refman}
BuildRequires:	texlive-collection-fontsrecommended
%if 0%{?fedora}
BuildRequires:	texlive-collection-langcyrillic
BuildRequires:	texlive-collection-langportuguese
BuildRequires:	texlive-newunicodechar
%endif
BuildRequires:	texlive-epstopdf
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
%endif
BuildRequires:	unixODBC-devel

%if 0%{?suse_version}
%if 0%{?suse_version} <= 1315
BuildRequires:	java-1_8_0-openjdk-devel
%else
BuildRequires:	java-11-openjdk-devel
%endif
%endif

%if 0%{?suse_version} >= 1315
BuildRequires:	hdf hdf-devel hdf-devel-static
BuildRequires:	hdf5 hdf5-devel hdf5-devel-static
BuildRequires:	libexpat-devel libjson-c-devel
BuildRequires:	libjasper-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	python3-numpy-devel
%else
BuildRequires:	g2clib-static
BuildRequires:	libdap-devel
BuildRequires:	expat-devel
BuildRequires:	hdf-devel hdf-static hdf5-devel
BuildRequires:	jasper-devel
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	json-c-devel
BuildRequires:	libdap-devel libgta-devel
BuildRequires:	librx-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	xerces-c-devel
%endif
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	libtirpc-devel

BuildRequires:	python3-devel

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	python36-numpy
%else
BuildRequires:	python3-numpy
%endif
BuildRequires:	python3-setuptools

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# We have multilib triage
%if "%{_lib}" == "lib"
  %global cpuarch 32
%else
  %global cpuarch 64
%endif

#TODO: Description on the lib?
%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:	Development files for the GDAL file format library

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-static < 1.9.0-1

%description devel
This package contains development files for GDAL.


%package libs
Summary:	GDAL file format library
# https://trac.osgeo.org/gdal/ticket/3978#comment:5
Obsoletes:	%{name}-ruby < 1.11.0-1

# proj DL-opened in ogrct.cpp, see also fix in %%prep
Requires:	proj%{projmajorversion} >= %{projfullversion}

Requires:	geos%{geosmajorversion} ogdi%{ogdimajorversion}
Requires:	netcdf gpsbabel
Requires:	libgeotiff%{libgeotiffmajorversion}-devel
Requires:	libspatialite%{libspatialitemajorversion}-devel

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1400
# These packages come from science repo:
# https://download.opensuse.org/repositories/science
Requires:	libarmadillo11 libnetcdf19
%endif
%endif
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 7
Requires:	armadillo
%endif

%description libs
This package contains the GDAL file format library.

%package doc
Summary:	Documentation for GDAL
BuildArch:	noarch

%description doc
This package contains HTML and PDF documentation for GDAL.

%package python3
%{?python_provide:%python_provide python3-gdal}
Summary:	Python modules for the GDAL file format library
Requires:	python3-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	gdal-python3 < 2.3.1
Provides:	gdal-python3 = %version-%release

%description python3
The GDAL Python 3 modules provide support to handle multiple GIS file formats.

%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	%{name}-python3

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$

%prep
%setup -q -n %{sname}-%{version}-fedora

pushd gdal
# Delete bundled libraries
%{__rm} -rf frmts/zlib
%{__rm} -rf frmts/png/libpng
%{__rm} -rf frmts/gif/giflib
%{__rm} -rf frmts/jpeg/libjpeg \
    frmts/jpeg/libjpeg12
%{__rm} -rf frmts/gtiff/libgeotiff \
    frmts/gtiff/libtiff
#rm -r frmts/grib/degrib/g2clib

# For patch16:
autoreconf

%patch -P 8 -p0 -b .java~
%patch -P 12 -p0
%patch -P 13 -p0

%patch -P 16 -p0

# Copy in PROVENANCE.TXT-fedora
cp -p %SOURCE2 .


# Replace hard-coded library- and include paths
sed -i 's|-L\$with_cfitsio -L\$with_cfitsio/lib -lcfitsio|-lcfitsio|g' configure
sed -i 's|-I\$with_cfitsio -I\$with_cfitsio/include|-I\$with_cfitsio/include/cfitsio|g' configure
sed -i 's|-L\$with_netcdf -L\$with_netcdf/lib -lnetcdf|-lnetcdf|g' configure
%if 0%{?suse_version} >= 1315
:
%else
sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
%endif
sed -i 's|-L\$with_ogdi -L\$with_ogdi/lib -logdi|-logdi|g' configure
sed -i 's|-L\$with_jpeg -L\$with_jpeg/lib -ljpeg|-ljpeg|g' configure
sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure

# libproj is dlopened; upstream sources point to .so, which is usually not present
# http://trac.osgeo.org/gdal/ticket/3602
sed -i 's|libproj.so|libproj.so.%{proj_somaj}|g' ogr/ogrct.cpp

# Adjust check for LibDAP version
# http://trac.osgeo.org/gdal/ticket/4545
%if %cpuarch == 64
  sed -i 's|with_dods_root/lib|with_dods_root/lib64|' configure
%endif

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

# Add our custom cflags when trying to find geos
# https://bugzilla.redhat.com/show_bug.cgi?id=1284714
sed -i 's|CFLAGS=\"${GEOS_CFLAGS}\"|CFLAGS=\"${CFLAGS} ${GEOS_CFLAGS}\"|g' configure
popd

%build
#TODO: Couldn't I have modified that in the prep section?
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
export CPPFLAGS="$CPPFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
LDFLAGS="$LDFLAGS -L%{projinstdir}/lib -L%{ogdiinstdir}/lib -L%{libgeotiffinstdir}/lib -L%{geosinstdir}/lib64 -L%{libspatialiteinstdir}/lib -L%{sqlitelibdir}"; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib,%{ogdiinstdir}/lib,%{libgeotiffinstdir}/lib,%{geosinstdir}/lib64,%{libspatialiteinstdir}/lib" ; export SHLIB_LINK
export OGDI_CFLAGS='-I%{ogdiinstdir}/include/ogdi'
export OGDI_INCLUDE='-I%{ogdiinstdir}/include/ogdi'
export OGDI_LIBS='-L%{ogdiinstdir}/lib'

# For future reference:
# epsilon: Stalled review -- https://bugzilla.redhat.com/show_bug.cgi?id=660024
# Building without pgeo driver, because it drags in Java

%if 0%{?g2clib_enabled}
 %if 0%{?fedora} >= 35
 %global g2clib g2c_v1.6.3
 %endif
 %if 0%{?rhel} == 8
 %global g2clib g2c_v1.6.0
 %endif
 %if 0%{?rhel} == 7
 %global g2clib grib2c
 %endif
 %if 0%{?rhel} == 9
 %global g2clib g2c_v1.6.3
 %endif
 %if 0%{?suse_version} >= 1315
 %global g2clib grib2c
 %endif
%endif

pushd gdal
./configure \
%if 0%{?g2clib_enabled}
	LIBS="-l%{g2clib} -ltirpc" \
%else
	LIBS="-ltirpc" \
%endif
	--prefix=%{gdalinstdir}	\
	--bindir=%{gdalinstdir}/bin	\
	--sbindir=%{gdalinstdir}/sbin	\
	--libdir=%{gdalinstdir}/lib	\
	--datadir=%{gdalinstdir}/share	\
	--datarootdir=%{gdalinstdir}/share	\
	--with-armadillo	\
	--with-curl		\
	--with-cfitsio=%{_prefix}	\
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 7 || 0%{?suse_version} <= 1499
	--with-dods-root=%{_prefix}	\
	LIBS="-l%{g2clib} -ltirpc" \
%endif
	--with-expat		\
	--with-freexl		\
	--with-geos=%{geosinstdir}/bin/geos-config	\
	--with-geotiff=%{libgeotiffinstdir}	\
	--with-gif		\
%if 0%{?suse_version} >= 1315
	--without-gta		\
%else
	--with-gta		\
%endif
	--with-hdf4		\
	--with-hdf5		\
	--with-jasper		\
%if 0%{?suse_version} >= 1315
	--without-java		\
%else
	--with-java		\
%endif
	--with-jpeg		\
	--with-libjson-c	\
	--without-jpeg12	\
	--with-liblz4		\
	--with-liblzma		\
	--with-libtiff=external	\
	--with-libz		\
	--without-mdb		\
	%{mysql}		\
	--with-netcdf		\
	--with-odbc		\
	--with-ogdi=%{ogdiinstdir}	\
	--without-msg		\
	--with-openjpeg		\
	--with-pcraster		\
	--with-pg=yes		\
	--with-png		\
	%{poppler}		\
	--with-proj=%{projinstdir}	\
	%{spatialite}		\
%if 0%{?rhel} && 0%{?rhel} == 7
	--disable-driver-elastic \
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
	--with-sqlite3=%{sqlitelibdir}	\
%else
	--with-sqlite3		\
%endif
	--with-threads		\
%if 0%{?fedora}
	--with-libkml		\
%endif
	--with-webp		\
	--with-xerces		\
	--enable-shared

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# {?_smp_mflags} doesn't work; Or it does -- who knows!
# NOTE: running autoconf seems to break build:
# fitsdataset.cpp:37:10: fatal error: fitsio.h: No such file or directory
# #include <fitsio.h>

POPPLER_OPTS="POPPLER_0_20_OR_LATER=yes POPPLER_0_23_OR_LATER=yes POPPLER_BASE_STREAM_HAS_TWO_ARGS=yes"
%if 0%{?fedora} > 30 || 0%{?rhel} > 7
POPPLER_OPTS="$POPPLER_OPTS POPPLER_0_58_OR_LATER=yes"
%endif
export SHLIB_LINK="$SHLIB_LINK"
%{__make} %{?_smp_mflags} $POPPLER_OPTS

# Build some utilities, as requested in BZ #1271906
pushd ogr/ogrsf_frmts/s57/
  %{__make} %{?_smp_mflags} all
popd

# Make Python modules
pushd swig/python
  %py3_build
popd

popd

%install
%{__rm} -rf %{buildroot}

export CXXFLAGS="$CFLAGS -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
export CPPFLAGS="$CPPFLAGS -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
LDFLAGS="$LDFLAGS -L%{ogdiinstdir}/lib -L%{libgeotiffinstdir}/lib -L%{geosinstdir}/lib64 -L%{libspatialiteinstdir}/lib -L%{sqlitelibdir}"; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{ogdiinstdir}/lib,%{libgeotiffinstdir}/lib,%{geosinstdir}/lib64,%{libspatialiteinstdir}/lib" ; export SHLIB_LINK
export OGDI_CFLAGS='-I%{ogdiinstdir}/include/ogdi'
export OGDI_INCLUDE='-I%{ogdiinstdir}/include/ogdi'
export OGDI_LIBS='-L%{ogdiinstdir}/lib'

pushd gdal
# Starts here
SHLIB_LINK="$SHLIB_LINK" make %{?_smp_mflags} DESTDIR=%{buildroot}	\
	install	\
	install-man

%{__install} -pm 755 ogr/ogrsf_frmts/s57/s57dump %{buildroot}%{gdalinstdir}/bin

# Directory for auto-loading plugins
%{__mkdir} -p %{buildroot}%{_libdir}/%{name}plugins

# Install formats documentation
for dir in frmts ogr/ogrsf_frmts ogr; do
  %{__mkdir} -p $dir
  find $dir -name "*.html" -exec install -p -m 644 '{}' $dir \;
done

#TODO: Header date lost during installation
# Install multilib cpl_config.h bz#430894
%{__install} -p -D -m 644 port/cpl_config.h %{buildroot}%{gdalinstdir}/include/cpl_config-%{cpuarch}.h
# Create universal multilib cpl_config.h bz#341231
# The problem is still there in 1.9.
#TODO: Ticket?

#>>>>>>>>>>>>>
cat > %{buildroot}%{gdalinstdir}/include/cpl_config.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "cpl_config-32.h"
#else
#if __WORDSIZE == 64
#include "cpl_config-64.h"
#else
#error "Unknown word size"
#endif
#endif
EOF
#<<<<<<<<<<<<<
touch -r NEWS.md port/cpl_config.h

# Create and install pkgconfig file
#TODO: Why does that exist? Does Grass really use it? I don't think so.
# http://trac.osgeo.org/gdal/ticket/3470
#>>>>>>>>>>>>>
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: GDAL
Description: GIS file format library
Version: %{version}
Libs: -L\${libdir} -lgdal
Cflags: -I\${includedir}/%{name}
EOF
#<<<<<<<<<<<<<
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/
touch -r NEWS.md %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Multilib gdal-config
# Rename the original script to gdal-config-$arch (stores arch-specific information)
# and create a script to call one or the other -- depending on detected architecture
# TODO: The extra script will direct you to 64 bit libs on
# 64 bit systems -- whether you like that or not
mv %{buildroot}%{gdalinstdir}/bin/%{sname}-config %{buildroot}%{gdalinstdir}/bin/%{sname}-config-%{cpuarch}
#>>>>>>>>>>>>>
cat > %{buildroot}%{gdalinstdir}/bin/%{sname}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
%{gdalinstdir}/bin/%{sname}-config-64 \${*}
;;
*)
%{gdalinstdir}/bin/%{sname}-config-32 \${*}
;;
esac
EOF
#<<<<<<<<<<<<<
touch -r NEWS.md %{buildroot}%{gdalinstdir}/bin/%{sname}-config
chmod 755 %{buildroot}%{gdalinstdir}/bin/%{sname}-config

# Clean up junk
%{__rm} -f %{buildroot}%{gdalinstdir}/bin/*.dox

#jni-libs and libgdal are also built static (*.a)
#.exists and .packlist stem from Perl
for junk in {*.a,*.la,*.bs,.exists,.packlist} ; do
  find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

# Don't duplicate license files
%{__rm} -f %{buildroot}%{_datadir}/%{name}/LICENSE.TXT

# Install some files manually, per yet-another-broken-change in 3.4.2:

%{__mkdir} -p %{buildroot}%{_docdir}/%{name}-libs
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}-python3
%{__cp} LICENSE.TXT NEWS.md PROVENANCE.TXT COMMITTERS %{buildroot}%{_docdir}/%{name}-libs
%{__cp} swig/python/gdal-utils/README.rst %{buildroot}%{_docdir}/%{name}-python3

# Throw away random API man mages plus artefact seemingly caused by Doxygen 1.8.1 or 1.8.1.1
for f in 'GDAL*' BandProperty ColorAssociation CutlineTransformer DatasetProperty EnhanceCBInfo ListFieldDesc NamedColor OGRSplitListFieldLayer VRTBuilder; do
  %{__rm} -rf %{buildroot}%{gdalinstdir}/share/man/man1/$f.1*
done

#TODO: What's that?
%{__rm} -f %{buildroot}%{gdalinstdir}/share/man/man1/*_%{name}-%{version}-fedora_apps_*
%{__rm} -f %{buildroot}%{gdalinstdir}/share/man/man1/_home_rouault_dist_wrk_gdal_apps_.1*

# PGDG: Move includes under gdalinst directory:
%{__mkdir} -p %{buildroot}%{gdalinstdir}/include
%{__mkdir} -p %{buildroot}%{gdalinstdir}/share/man

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE3} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

pushd swig/python
  %py3_install
popd

popd

%check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{gdalinstdir}/bin/gdallocationinfo
%{gdalinstdir}/bin/gdal_contour
%{gdalinstdir}/bin/gdal_create
%{gdalinstdir}/bin/gdal_rasterize
%{gdalinstdir}/bin/gdal_translate
%{gdalinstdir}/bin/gdaladdo
%{gdalinstdir}/bin/gdalinfo
%{gdalinstdir}/bin/gdaldem
%{gdalinstdir}/bin/gdalbuildvrt
%{gdalinstdir}/bin/gdaltindex
%{gdalinstdir}/bin/gdalwarp
%{gdalinstdir}/bin/gdal_grid
%{gdalinstdir}/bin/gdalenhance
%{gdalinstdir}/bin/gdalmanage
%{gdalinstdir}/bin/gdalsrsinfo
%{gdalinstdir}/bin/gdaltransform
%{gdalinstdir}/bin/gdal_viewshed
%{gdalinstdir}/bin/gdalmdiminfo
%{gdalinstdir}/bin/gdalmdimtranslate
%{gdalinstdir}/bin/nearblack
%{gdalinstdir}/bin/ogr*
%{gdalinstdir}/bin/s57*
%{gdalinstdir}/bin/gnmanalyse
%{gdalinstdir}/bin/gnmmanage

%files libs
%if 0%{?rhel} == 7
%{_docdir}/%{name}-libs/COMMITTERS
%{_docdir}/%{name}-libs/LICENSE.TXT
%{_docdir}/%{name}-libs/NEWS.md
%{_docdir}/%{name}-libs/PROVENANCE.TXT
%else
%doc LICENSE.TXT NEWS.md PROVENANCE.TXT COMMITTERS
%endif
%{gdalinstdir}/lib/libgdal.so.%{gdalsomajorversion}
%{gdalinstdir}/lib/libgdal.so.%{gdalsomajorversion}.*
%{gdalinstdir}/share/
#TODO: Possibly remove files like .dxf, .dgn, ...
%dir %{gdalinstdir}/lib/%{sname}plugins
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%{gdalinstdir}/bin/%{sname}-config
%{gdalinstdir}/bin/%{sname}-config-%{cpuarch}
%dir %{gdalinstdir}/include/
%{gdalinstdir}/include/*.h
%{gdalinstdir}/lib/*.so
%{gdalinstdir}/lib/pkgconfig/%{sname}.pc
%{_libdir}/pkgconfig/%{name}.pc

%files doc

%files python3
%if 0%{?rhel} == 7
%{_docdir}/%{name}-python3/README.rst
%else
%doc swig/python/README.rst
%endif
%{python3_sitearch}/osgeo
%{python3_sitearch}/osgeo_utils
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/

%files python-tools
%_bindir/*.py

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-8.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Tue Jan 10 2023 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-8
- Rebuild against libnetcdf19 on SLES 15.

* Sun Jan 8 2023 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-7
- Use libspatialite50 on SLES 15. This is a followup commit
  to fix PostGIS issues on SLES 15, and 7ae8e6b9ba8.

* Sun Nov 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-6
- RHEL 8 includes poppler-devel, so no need for our version.

* Wed Oct 19 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-5
- Add gc2lib version for Fedora 37, remove old versions.

* Wed Jul 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-4
- Fix RHEL 7 builds (extremely ugly hack, though)

* Wed Jul 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-3
- Add RHEL 9 support and fix Fedora 36 support.

* Sun Jun 12 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-2
- Rebuild against new armadillo on RHEL 8

* Fri May 6 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.3-1
- Update to 3.4.3, per changes described at:
  https://github.com/OSGeo/gdal/blob/v3.4.3/gdal/NEWS.md

* Mon Mar 14 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.2-1
- Update to 3.4.2, per changes described at:
  https://github.com/OSGeo/gdal/blob/v3.4.2/gdal/NEWS.md
- Move some logic in the spec file to gdal-cleaner.sh in order
  to avoid losing time during each build attempt.

* Wed Jan 19 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.1-3
- Fix dependency on RHEL 7.

* Sat Jan 8 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.1-2
- Build against PROJ 8.2.x and GeOS 3.10.x

* Fri Jan 7 2022 Devrim Gunduz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1

* Wed Dec 15 2021 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-2
- Add Requires for armadillo package, per
  https://redmine.postgresql.org/issues/7076

* Tue Nov 30 2021 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-1
- Initial 3.4.0 packaging for the PostgreSQL RPM repository, per:
  https://github.com/OSGeo/gdal/blob/v3.4.0/gdal/NEWS.md
