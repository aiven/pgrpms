%global pgmajorversion 11
%global sname gdal
%global gdalinstdir /usr/%{name}

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

# Major digit of the proj so version
%global proj_somaj 13

# Tests can be of a different version
%global testversion 2.3.2
%global run_tests 0

%global bashcompletiondir %(pkg-config --variable=compatdir bash-completion)

%if 0%{?bootstrap}
%global build_refman 0
%global with_mysql 0
%global mysql --without-mysql
%global with_poppler 0
%global poppler --without-poppler
%global with_spatialite 0
%global spatialite --without-spatialite
%else
# Enable/disable generating refmans
# texlive currently broken deps and FTBFS in rawhide
%global build_refman 1
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492
%global with_mysql 1
%global mysql --with-mysql
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492
%global with_poppler 1
%global poppler --with-poppler
%global with_spatialite 1
%global spatialite "--with-spatialite"
%endif

%bcond_with python2
%bcond_without python3

# No ppc64 build for spatialite in EL6
# https://bugzilla.redhat.com/show_bug.cgi?id=663938
%if 0%{?rhel} == 6
%ifnarch ppc64
%global with_spatialite 0
%global spatialite --without-spatialite
%endif
%endif

Name:		%{sname}23
Version:	2.3.2
Release:	7%{?dist}%{?bootstrap:.%{bootstrap}.bootstrap}
Summary:	GIS file format library
License:	MIT
URL:		http://www.gdal.org
# Source0:   http://download.osgeo.org/gdal/%%{version}/gdal-%%{version}.tar.xz
# See PROVENANCE.TXT-fedora and the cleaner script for details!

Source0:	%{sname}-%{version}-fedora.tar.xz
Source1:	http://download.osgeo.org/%{name}/%{testversion}/%{sname}autotest-%{testversion}.tar.gz

# Cleaner script for the tarball
Source3:	%{sname}-cleaner.sh

Source4:	PROVENANCE.TXT-fedora

# Patch to use system g2clib
Patch1:		%{sname}-g2clib.patch
# Patch for Fedora JNI library location
Patch2:		%{sname}-jni.patch
# Fix bash-completion install dir
Patch3:		%{sname}-completion.patch

# Fedora uses Alternatives for Java
Patch8:		%{sname}-1.9.0-java.patch

Patch9:		%{sname}-2.3.0-zlib.patch

# https://github.com/OSGeo/gdal/pull/876
Patch10:	%{sname}-2.3.1-perl-build.patch

Patch11:	%{sname}-2.3.2-poppler-0.73.0.patch


BuildRequires:	gcc gcc-c++
BuildRequires:	ant
# No armadillo in EL5
BuildRequires:	armadillo-devel
BuildRequires:	bash-completion
BuildRequires:	cfitsio-devel
# No CharLS in EL5
#BuildRequires: CharLS-devel
BuildRequires:	chrpath
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	fontconfig-devel
# No freexl in EL5
BuildRequires:	freexl-devel
BuildRequires:	g2clib-static
BuildRequires:	geos-devel >= 3.7.1
BuildRequires:	ghostscript
BuildRequires:	hdf-devel
BuildRequires:	hdf-static
BuildRequires:	hdf5-devel
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	jasper-devel
BuildRequires:	jpackage-utils
# For 'mvn_artifact' and 'mvn_install'
BuildRequires:	javapackages-local
BuildRequires:	json-c-devel
BuildRequires:	libgeotiff-devel
# No libgta in EL5
BuildRequires:	libgta-devel

BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
# No libkml in EL
BuildRequires:	libkml-devel

%if %{with_spatialite}
BuildRequires:	libspatialite-devel
%endif

BuildRequires:	libtiff-devel
# No libwebp in EL 5 and 6
BuildRequires:	libwebp-devel
BuildRequires:	libtool
BuildRequires:	giflib-devel
BuildRequires:	netcdf-devel
BuildRequires:	libdap-devel
BuildRequires:	librx-devel
%if 0%{?with_mysql}
BuildRequires:	mariadb-connector-c-devel
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	pcre-devel
BuildRequires:	ogdi-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	openjpeg2-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	%{_bindir}/pkg-config
%if 0%{?with_poppler}
BuildRequires:	poppler-devel
%endif
BuildRequires:	proj-devel >= 5.2.0
%if %{with python2}
BuildRequires:	python2-devel
BuildRequires:	python2-numpy
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-numpy
%endif
BuildRequires:	sqlite-devel
BuildRequires:	swig
%if %{build_refman}
BuildRequires:	texlive-latex
BuildRequires:	texlive-collection-fontsrecommended
%if 0%{?fedora}
BuildRequires:	texlive-collection-langcyrillic
BuildRequires:	texlive-collection-langportuguese
BuildRequires:	texlive-newunicodechar
%endif
BuildRequires:	texlive-collection-latex
BuildRequires:	texlive-epstopdf
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tabu.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
%endif
BuildRequires:	unixODBC-devel
BuildRequires:	xerces-c-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	libtirpc-devel

# Run time dependency for gpsbabel driver
Requires:	gpsbabel

# proj DL-opened in ogrct.cpp, see also fix in %%prep
%if 0%{?__isa_bits} == 64
Requires:	libproj.so.%{proj_somaj}()(64bit)
%else
Requires:	libproj.so.%{proj_somaj}
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# We have multilib triage
%if "%{_lib}" == "lib"
  %global cpuarch 32
%else
  %global cpuarch 64
%endif

%if ! (0%{?fedora} || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
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

# Old rpm didn't figure out
%if 0%{?rhel} < 6
Requires: pkgconfig
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-static < 1.9.0-1

%description devel
This package contains development files for GDAL.


%package libs
Summary:	GDAL file format library
# https://trac.osgeo.org/gdal/ticket/3978#comment:5
Obsoletes:	%{name}-ruby < 1.11.0-1

%description libs
This package contains the GDAL file format library.


%package java
Summary:	Java modules for the GDAL file format library
Requires:	jpackage-utils
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description java
The GDAL Java modules provide support to handle multiple GIS file formats.


%package javadoc
Summary:	Javadocs for %{name}
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
This package contains the API documentation for %{name}.


%package perl
Summary:	Perl modules for the GDAL file format library
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
The GDAL Perl modules provide support to handle multiple GIS file formats.

%if %{with python2}
%package -n python2-gdal
%{?python_provide:%python_provide python2-gdal}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary:	Python modules for the GDAL file format library
Requires:	numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description -n python2-gdal
The GDAL Python modules provide support to handle multiple GIS file formats.
The package also includes a couple of useful utilities in Python.
%endif


%if %{with python3}
%package -n python3-gdal
%{?python_provide:%python_provide python3-gdal}
Summary:	Python modules for the GDAL file format library
Requires:	python3-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	gdal-python3 < 2.3.1
Provides:	gdal-python3 = %version-%release

%description -n python3-gdal
The GDAL Python 3 modules provide support to handle multiple GIS file formats.
%endif


%if %{with python2} || %{with python3}
%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	%{?with_python3:python3-gdal}%{?!with_python3:python2-gdal}

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library
%endif


%package doc
Summary:	Documentation for GDAL
BuildArch:	noarch

%description doc
This package contains HTML and PDF documentation for GDAL.

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$

%prep
%setup -q -n %{sname}-%{version}-fedora -a 1

# Delete bundled libraries
rm -rf frmts/zlib
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg \
    frmts/jpeg/libjpeg12
rm -rf frmts/gtiff/libgeotiff \
    frmts/gtiff/libtiff
#rm -r frmts/grib/degrib/g2clib

#%%patch1 -p1 -b .g2clib~
#%%patch2 -p1 -b .jni~
%patch3 -p1 -b .completion~
%patch8 -p1 -b .java~
%patch9 -p1 -b .zlib~
%patch10 -p1 -b .perl-build~
%patch11 -p1 -b .poppler-0.73.0

# Copy in PROVENANCE.TXT-fedora
cp -p %SOURCE4 .

# Sanitize linebreaks and encoding
#TODO: Don't touch data directory!
# /frmts/grib/degrib18/degrib/metaname.cpp
# and geoconcept.c are potentially dangerous to change
set +x
for f in `find . -type f` ; do
  if file $f | grep -q ISO-8859 ; then
    set -x
    iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
      mv -f ${f}.tmp $f
    set +x
  fi
  if file $f | grep -q CRLF ; then
    set -x
    sed -i -e 's|\r||g' $f
    set +x
  fi
done
set -x

for f in apps; do
pushd $f
  chmod 644 *.cpp
popd
done

# Replace hard-coded library- and include paths
sed -i 's|-L\$with_cfitsio -L\$with_cfitsio/lib -lcfitsio|-lcfitsio|g' configure
sed -i 's|-I\$with_cfitsio -I\$with_cfitsio/include|-I\$with_cfitsio/include/cfitsio|g' configure
sed -i 's|-L\$with_netcdf -L\$with_netcdf/lib -lnetcdf|-lnetcdf|g' configure
sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
sed -i 's|-L\$with_ogdi -L\$with_ogdi/lib -logdi|-logdi|g' configure
sed -i 's|-L\$with_jpeg -L\$with_jpeg/lib -ljpeg|-ljpeg|g' configure
sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure

# libproj is dlopened; upstream sources point to .so, which is usually not present
# http://trac.osgeo.org/gdal/ticket/3602
sed -i 's|libproj.so|libproj.so.%{proj_somaj}|g' ogr/ogrct.cpp

%if %{with python3} || %{with python2}
# Fix Python samples to depend on correct interpreter
mkdir -p swig/python3/samples
pushd swig/python/samples
for f in `find . -name '*.py'`; do
  sed 's|^#!.\+python$|#!/usr/bin/python3|' $f > ../../python3/samples/$f
  chmod --reference=$f ../../python3/samples/$f
  sed -i 's|^#!.\+python$|#!/usr/bin/python2|' $f
done
popd
%endif

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

%build
#TODO: Couldn't I have modified that in the prep section?
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS -I%{_includedir}/libgeotiff -I%{_includedir}/tirpc"
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/libgeotiff -I%{_includedir}/tirpc"

# For future reference:
# epsilon: Stalled review -- https://bugzilla.redhat.com/show_bug.cgi?id=660024
# Building without pgeo driver, because it drags in Java

%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
%global g2clib g2c_v1.6.0
%else
%global g2clib grib2c
%endif

%configure \
	LIBS="-l%{g2clib} -ltirpc" \
	--prefix=%{gdalinstdir}	\
	--bindir=%{gdalinstdir}/bin	\
	--sbindir=%{gdalinstdir}/sbin	\
	--libdir=%{gdalinstdir}/lib	\
	--datadir=%{gdalinstdir}/share	\
	--datarootdir=%{gdalinstdir}/share	\
	--with-autoload=%{_libdir}/%{name}plugins \
	--with-armadillo	\
	--with-curl		\
	--with-cfitsio=%{_prefix}	\
	--with-dods-root=%{_prefix}	\
	--with-expat		\
	--with-freexl		\
	--with-geos		\
	--with-geotiff=external	\
	--with-gif		\
	--with-gta		\
	--with-hdf4		\
	--with-hdf5		\
	--with-jasper		\
	--with-java		\
	--with-jpeg		\
	--with-libjson-c	\
	--without-jpeg12	\
	--with-liblzma		\
	--with-libtiff=external	\
	--with-libz		\
	--without-mdb		\
	%{mysql}		\
	--with-netcdf		\
	--with-odbc		\
	--with-ogdi		\
	--without-msg		\
	--with-openjpeg		\
	--with-pcraster		\
	--with-pg=%{pginstdir}/bin/pg_config	\
	--with-png		\
	%{poppler}		\
	%{spatialite}		\
	--with-sqlite3		\
	--with-threads		\
	--with-webp		\
	--with-xerces		\
	--enable-shared		\
	--with-libkml

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# {?_smp_mflags} doesn't work; Or it does -- who knows!
# NOTE: running autoconf seems to break build:
# fitsdataset.cpp:37:10: fatal error: fitsio.h: No such file or directory
#  #include <fitsio.h>

POPPLER_OPTS="POPPLER_0_20_OR_LATER=yes POPPLER_0_23_OR_LATER=yes POPPLER_BASE_STREAM_HAS_TWO_ARGS=yes"
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
POPPLER_OPTS="$POPPLER_OPTS POPPLER_0_58_OR_LATER=yes"
%endif

make %{?_smp_mflags} $POPPLER_OPTS

make man
make docs

# Build some utilities, as requested in BZ #1271906
pushd ogr/ogrsf_frmts/s57/
  make all
popd

pushd frmts/iso8211/
  make all
popd

# Make Java module and documentation
pushd swig/java
  make
  ant maven
popd

%mvn_artifact swig/java/build/maven/gdal-%version.pom swig/java/build/maven/gdal-%version.jar

# Make Python modules
pushd swig/python
  %{?with_python2:%py2_build}
  %{?with_python3:%py3_build}
popd

# Make Python modules
pushd swig/perl
  perl Makefile.PL INSTALLDIRS=vendor
  %make_build
popd

# --------- Documentation ----------

# No useful documentation in swig
%global docdirs apps doc doc/br doc/ru ogr ogr/ogrsf_frmts frmts/gxf frmts/iso8211 frmts/pcidsk frmts/sdts frmts/vrt ogr/ogrsf_frmts/dgn/
for docdir in %{docdirs}; do
  # CreateHTML and PDF documentation, if specified
  pushd $docdir
    if [ ! -f Doxyfile ]; then
      doxygen -g
    else
      doxygen -u
    fi
    sed -i -e 's|^GENERATE_LATEX|GENERATE_LATEX = YES\n#GENERATE_LATEX |' Doxyfile
    sed -i -e 's|^GENERATE_HTML|GENERATE_HTML = YES\n#GENERATE_HTML |' Doxyfile
    sed -i -e 's|^USE_PDFLATEX|USE_PDFLATEX = YES\n#USE_PDFLATEX |' Doxyfile

    if [ $docdir == "doc/ru" ]; then
      sed -i -e 's|^OUTPUT_LANGUAGE|OUTPUT_LANGUAGE = Russian\n#OUTPUT_LANGUAGE |' Doxyfile
    fi
    rm -rf latex html
    doxygen

    %if %{build_refman}
      pushd latex
	sed -i -e '/rfoot\[/d' -e '/lfoot\[/d' doxygen.sty
	sed -i -e '/small/d' -e '/large/d' refman.tex
	sed -i -e 's|pdflatex|pdflatex -interaction nonstopmode |g' Makefile
	make refman.pdf || true
      popd
    %endif
  popd
done


%install
rm -rf %{buildroot}

pushd swig/python
  %{?with_python2:%py2_install}
  %{?with_python3:%py3_install}
popd

pushd swig/perl
  %make_install
popd

make	DESTDIR=%{buildroot}	\
	install	\
	install-man

%{__install} -pm 755 ogr/ogrsf_frmts/s57/s57dump %{buildroot}%{gdalinstdir}/bin
%{__install} -pm 755 frmts/iso8211/8211createfromxml %{buildroot}%{gdalinstdir}/bin
%{__install} -pm 755 frmts/iso8211/8211dump %{buildroot}%{gdalinstdir}/bin
%{__install} -pm 755 frmts/iso8211/8211view %{buildroot}%{gdalinstdir}/bin

# Directory for auto-loading plugins
mkdir -p %{buildroot}%{_libdir}/%{name}plugins

#TODO: Don't do that?
find %{buildroot}%{perl_vendorarch} -name "*.dox" -exec rm -rf '{}' \;
%{__rm} %{buildroot}%{perl_archlib}/perllocal.pod

%if %{without python} && %{without python3}
%{__rm} %buildroot%_mandir/man1/{pct2rgb,rgb2pct}.1
%endif

# Correct permissions
#TODO and potential ticket: Why are the permissions not correct?
find %{buildroot}%{perl_vendorarch} -name "*.so" -exec chmod 755 '{}' \;
find %{buildroot}%{perl_vendorarch} -name "*.pm" -exec chmod 644 '{}' \;

# install Java plugin
%mvn_install -J swig/java/java

# 775 on the .so?
# copy JNI libraries and links, non versioned link needed by JNI
# What is linked here?
%{__mkdir} -p %{buildroot}%{_jnidir}/%{name}
%{__cp} -pl swig/java/.libs/*.so*  \
    %{buildroot}%{_jnidir}/%{name}/
chrpath --delete %{buildroot}%{_jnidir}/%{name}/*jni.so*

# Install Java API documentation in the designated place
%{__mkdir} -p %{buildroot}%{_javadocdir}/%{name}
%{__cp} -pr swig/java/java/org %{buildroot}%{_javadocdir}/%{name}

# Install refmans
for docdir in %{docdirs}; do
  pushd $docdir
    path=%{_builddir}/%{name}-%{version}-fedora/refman
    mkdir -p $path/html/$docdir
    cp -r html $path/html/$docdir

    # Install all Refmans
    %if %{build_refman}
	if [ -f latex/refman.pdf ]; then
		mkdir -p $path/pdf/$docdir
		cp latex/refman.pdf $path/pdf/$docdir
	fi
    %endif
  popd
done

# Install formats documentation
for dir in gdal_frmts ogrsf_frmts; do
  mkdir -p $dir
  find frmts -name "*.html" -exec install -p -m 644 '{}' $dir \;
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
#include "gdal/cpl_config-32.h"
#else
#if __WORDSIZE == 64
#include "gdal/cpl_config-64.h"
#else
#error "Unknown word size"
#endif
#endif
EOF
#<<<<<<<<<<<<<
touch -r NEWS port/cpl_config.h

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
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/
touch -r NEWS %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

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
%{gdalinstdir}/bin/%{name}-config-64 \${*}
;;
*)
%{gdalinstdir}/bin/%{name}-config-32 \${*}
;;
esac
EOF
#<<<<<<<<<<<<<
touch -r NEWS %{buildroot}%{gdalinstdir}/bin/%{sname}-config
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

# Throw away random API man mages plus artefact seemingly caused by Doxygen 1.8.1 or 1.8.1.1
for f in 'GDAL*' BandProperty ColorAssociation CutlineTransformer DatasetProperty EnhanceCBInfo ListFieldDesc NamedColor OGRSplitListFieldLayer VRTBuilder; do
  rm -rf %{buildroot}%{gdalinstdir}/share/man/man1/$f.1*
done

#TODO: What's that?
%{__rm} -f %{buildroot}%{gdalinstdir}/share/man/man1/*_%{name}-%{version}-fedora_apps_*
%{__rm} -f %{buildroot}%{gdalinstdir}/share/man/man1/_home_rouault_dist_wrk_gdal_apps_.1*

# PGDG: Move includes under gdalinst directory:
%{__mkdir} -p %{gdalinstdir}/include
%{__mkdir} -p %{gdalinstdir}/share
%{__mv} %{buildroot}%{_includedir}/* %{buildroot}%{gdalinstdir}/include
%{__mv} %{buildroot}%{_datadir}/* %{buildroot}%{gdalinstdir}/share

%check
%if %{run_tests}
for i in -I/usr/lib/jvm/java/include{,/linux}; do
    java_inc="$java_inc $i"
done


pushd %{name}autotest-%{testversion}
	# Export test enviroment
	export PYTHONPATH=$PYTHONPATH:%{buildroot}%{python_sitearch}
	#TODO: Nötig?
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
	# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%%{buildroot}%%{_libdir}:$java_inc

	export GDAL_DATA=%{buildroot}%{_datadir}/%{name}/

	# Enable these tests on demand
	#export GDAL_RUN_SLOW_TESTS=1
	#export GDAL_DOWNLOAD_TEST_DATA=1

	# Remove some test cases that would require special preparation
	rm -rf ogr/ogr_pg.py # No database available
	rm -rf ogr/ogr_mysql.py # No database available
	rm -rf osr/osr_esri.py # ESRI datum absent
	rm -rf osr/osr_erm.py # File from ECW absent

	# Run tests but force normal exit in the end
	./run_all.py || true
popd
%endif #%%{run_tests}


%ldconfig_scriptlets libs


%files
%{bashcompletiondir}/*
%{gdalinstdir}/bin/gdallocationinfo
%{gdalinstdir}/bin/gdal_contour
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
%{gdalinstdir}/bin/gdalserver
%{gdalinstdir}/bin/gdalsrsinfo
%{gdalinstdir}/bin/gdaltransform
%{gdalinstdir}/bin/nearblack
%{gdalinstdir}/bin/ogr*
%{gdalinstdir}/bin/8211*
%{gdalinstdir}/bin/s57*
%{gdalinstdir}/bin/testepsg
%{gdalinstdir}/bin/gnmanalyse
%{gdalinstdir}/bin/gnmmanage
%{gdalinstdir}/share/man/man1/gdal*.1*
%exclude %{gdalinstdir}/share/man/man1/gdal-config.1*
%exclude %{gdalinstdir}/share/man/man1/gdal2tiles.1*
%exclude %{gdalinstdir}/share/man/man1/gdal_fillnodata.1*
%exclude %{gdalinstdir}/share/man/man1/gdal_merge.1*
%exclude %{gdalinstdir}/share/man/man1/gdal_retile.1*
%exclude %{gdalinstdir}/share/man/man1/gdal_sieve.1*
%{gdalinstdir}/share/man/man1/nearblack.1*
%{gdalinstdir}/share/man/man1/ogr*.1*
%{gdalinstdir}/share/man/man1/gnm*.1

%files libs
%doc LICENSE.TXT NEWS PROVENANCE.TXT COMMITTERS PROVENANCE.TXT-fedora
%{gdalinstdir}/lib/libgdal.so.20
%{gdalinstdir}/lib/libgdal.so.20.*
%{gdalinstdir}/share/
#TODO: Possibly remove files like .dxf, .dgn, ...
%dir %{gdalinstdir}/lib/%{sname}plugins

%files devel
%{gdalinstdir}/bin/%{sname}-config
%{gdalinstdir}/bin/%{sname}-config-%{cpuarch}
%{gdalinstdir}/share/man/man1/gdal-config.1*
%dir %{gdalinstdir}/include/
%{gdalinstdir}/include/*.h
%{gdalinstdir}/lib/*.so
%{gdalinstdir}/lib/pkgconfig/%{name}.pc

# Can I even have a separate Java package anymore?
%files java -f .mfiles
%doc swig/java/apps
%{_jnidir}/%{name}/libgdalalljni.so*

%files javadoc -f .mfiles-javadoc

%files perl
%doc swig/perl/README
%{perl_vendorarch}/*
%{_mandir}/man3/*.3pm*

%if %{with python2}
%files -n python2-gdal
%doc swig/python/README.txt
%doc swig/python/samples
%{python2_sitearch}/osgeo
%{python2_sitearch}/GDAL-%{version}-py*.egg-info
%{python2_sitearch}/osr.py*
%{python2_sitearch}/ogr.py*
%{python2_sitearch}/gdal*.py*
%{python2_sitearch}/gnm.py*
%endif

%if %{with python3}
%files -n python3-gdal
%doc swig/python/README.txt
%doc swig/python3/samples
%{python3_sitearch}/osgeo
%{python3_sitearch}/GDAL-%{version}-py*.egg-info
%{python3_sitearch}/osr.py
%{python3_sitearch}/__pycache__/osr.*.py*
%{python3_sitearch}/ogr.py
%{python3_sitearch}/__pycache__/ogr.*.py*
%{python3_sitearch}/gdal*.py
%{python3_sitearch}/__pycache__/gdal*.*.py*
%{python3_sitearch}/gnm.py*
%{python3_sitearch}/__pycache__/gnm.*.py*
%endif

%if %{with python2} || %{with python3}
%files python-tools
%_bindir/*.py
%{gdalinstdir}/share/man/man1/pct2rgb.1*
%{gdalinstdir}/share/man/man1/rgb2pct.1*
%{gdalinstdir}/share/man/man1/gdal2tiles.1*
%{gdalinstdir}/share/man/man1/gdal_fillnodata.1*
%{gdalinstdir}/share/man/man1/gdal_merge.1*
%{gdalinstdir}/share/man/man1/gdal_retile.1*
%{gdalinstdir}/share/man/man1/gdal_sieve.1*
%endif

%files doc
%doc gdal_frmts ogrsf_frmts

#TODO: jvm
#Should be managed by the Alternatives system and not via ldconfig
#The MDB driver is said to require:
#Download jackcess-1.2.2.jar, commons-lang-2.4.jar and
#commons-logging-1.1.1.jar (other versions might work)
#If you didn't specify --with-jvm-lib-add-rpath at
#Or as before, using ldconfig

%changelog
* Tue Feb 05 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.2-7
- Drop Python 2 subpackage for mass Python 2 packages removal

* Mon Feb 04 2019 Pavel Raiskup <praiskup@redhat.com> - 2.3.2-6
- modernize java packaging (PR#9)

* Mon Feb 04 2019 Devrim Gündüz <devrim@gunduzorg> - 2.3.2-6
- Rebuild for new GeOS and Proj

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Marek Kasik <mkasik@redhat.com> - 2.3.2-4
- Additional fixes for the rebuild

* Fri Jan 25 2019 Marek Kasik <mkasik@redhat.com> - 2.3.2-3
- Rebuild for poppler-0.73.0

* Thu Oct 04 2018 Pavel Raiskup <praiskup@redhat.com> - 2.3.2-2
- Python 3 is the default Python now

* Mon Oct  1 2018 Volker Fröhlich <volker27@gmx.at> - 2.3.2-1
- New upstream release

* Mon Aug 27 2018 José Abílio Matos <jamatos@fc.up.pt> - 2.3.1-3
- rebuild for armadillo soname bump (take 2)

* Fri Aug 17 2018 José Abílio Matos <jamatos@fc.up.pt> - 2.3.1-2
- rebuild for armadillo soname bump

* Tue Aug 14 2018 Volker Fröhlich <volker27@gmx.at> - 2.3.1-1
- New upstream release

* Tue Aug 14 2018 Marek Kasik <mkasik@redhat.com> - 2.2.4-10
- Rebuild for poppler-0.67.0

* Wed Jul 25 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.4-9
- Fix #1606875

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.2.4-7
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.4-6
- Perl 5.28 rebuild

* Fri Jun 22 2018 Orion Poplawski <orion@nwra.com> - 2.2.4-5
- Rebuild for libdap 3.19.1

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.4-4
- Rebuilt for Python 3.7

* Sat May 26 2018 Christian Dersch <lupinix@mailbox.org> - 2.2.4-3
- rebuilt for cfitsio 3.450

* Tue Mar 27 2018 Björn Esser <besser82@fedoraproject.org> - 2.2.4-2
- Rebuilt for libjson-c.so.4 (json-c v0.13.1) on fc28

* Mon Mar 26 2018 Volker Fröhlich <volker27@gmx.at> - 2.2.4-1
- New upstream release

* Fri Mar 23 2018 Adam Williamson <awilliam@redhat.com> - 2.2.3-14
- Rebuild for poppler 0.63.0

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 2.2.3-13
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Fri Feb 23 2018 Christian Dersch <lupinix@mailbox.org> - 2.2.3-12
- rebuilt for cfitsio 3.420 (so version bump)

* Wed Feb 14 2018 David Tardon <dtardon@redhat.com> - 2.2.3-11
- rebuild for poppler 0.62.0

* Wed Feb 14 2018 Volker Fröhlich <volker27@gmx.at> - 2.2.3-10
- Don't own /etc/bash_completion.d (BZ#1545012)

* Tue Feb 13 2018 Pavel Raiskup <praiskup@redhat.com> - 2.2.3-9
- silence some rpmlint warnings

* Tue Feb 13 2018 Tom Hughes <tom@compton.nu> - 2.2.3-8
- Add patch for bug by node-gdal tests and fixed upstream

* Tue Feb 13 2018 Tom Hughes <tom@compton.nu> - 2.2.3-7
- Use libtirpc for RPC routines

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Than Ngo <than@redhat.com> - - 2.2.3-6
- cleanup condition

* Thu Dec 14 2017 Merlin Mathesius <mmathesi@redhat.com> - 2.2.3-5
- Cleanup spec file conditionals

* Thu Dec 14 2017 Pavel Raiskup <praiskup@redhat.com> - 2.2.3-4
- drop bootstrap mode
- build-require mariadb-connector-c-devel (rhbz#1494096)

* Mon Dec 11 2017 Björn Esser <besser82@fedoraproject.org> - 2.2.3-3.1.bootstrap
- Add patch to cleanly build against json-c v0.13

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 2.2.3-2.1.bootstrap
- Rebuilt for libjson-c.so.3

* Mon Dec 04 2017 Volker Froehlich <volker27@gmx.at> - 2.2.3-1
- New upstream release

* Wed Nov 29 2017 Volker Froehlich <volker27@gmx.at> - 2.2.2-2
- Re-enable bsb format (BZ#1432330)

* Fri Sep 22 2017 Volker Froehlich <volker27@gmx.at> - 2.2.2-1
- New upstream release
- Add new entries to the files sections

* Sun Sep 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.1.4-11
- rebuild (armadillo)

* Mon Sep 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.1.4-10
- support %%bootstrap mode, enable for rawhide (#1490492)
- segment POPPLER_OPTS, makes buildable on f25

* Fri Sep 08 2017 David Tardon <dtardon@redhat.com> - 2.1.4-9
- rebuild for poppler 0.59.0

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.4-8
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Orion Poplawski <orion@cora.nwra.com> - 2.1.4-7
- Handle new g2clib name in Fedora 27+

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.4-6
- Python 2 binary package renamed to python2-gdal
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 David Tardon <dtardon@redhat.com> - 2.1.4-5
- rebuild for poppler 0.57.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Adam Williamson <awilliam@redhat.com> - 2.1.4-2
- Rebuild against MariaDB 10.2
- BuildRequires: javapackages-local, for a macro that got moved there

* Sat Jul 01 2017 Volker Froehlich <volker27@gmx.at> - 2.1.4-1
- New upstream release

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.3-4
- Perl 5.26 rebuild

* Tue Mar 28 2017 David Tardon <dtardon@redhat.com> - 2.1.3-3
- rebuild for poppler 0.53.0

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 2.1.3-2
- Rebuild (libwebp)

* Fri Jan 27 2017 Volker Froehlich <volker27@gmx.at> - 2.1.3-1
- New upstream release
- Don't run tests by default (BZ #1260151)

* Tue Jan 24 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-6
- Rebuilt for proj 4.9.3
- Fix many rpmlint warnings/errors.
- Add a workaround for the pkg-config change in rawhide.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.2-5
- Rebuild for Python 3.6

* Fri Dec 16 2016 David Tardon <dtardon@redhat.com> - 2.1.2-4
- rebuild for poppler 0.50.0

* Thu Dec 01 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1.2-3
- Rebuild for jasper 2.0
- Add patch to fix build with jasper 2.0

* Wed Nov 23 2016 David Tardon <dtardon@redhat.com> - 2.1.2-2
- rebuild for poppler 0.49.0

* Sun Oct 30 2016 Volker Froehlich <volker27@gmx.at> - 2.1.2-1
- New upstream release

* Sat Oct 22 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-2
- Use system libjson-c

* Fri Oct 21 2016 Marek Kasik <mkasik@redhat.com> - 2.1.1-2
- Rebuild for poppler-0.48.0

* Fri Aug 12 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-1
- Update to 2.1.1
- Add patch to fix bash-completion installation and install it (bug #1337143)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Marek Kasik <mkasik@redhat.com> - 2.1.0-7
- Rebuild for poppler-0.45.0

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.0-6
- Perl 5.24 rebuild

* Mon May 09 2016 Volker Froehlich <volker27@gmx.at> - 2.1.0-5
- Add missing BR for libkml

* Fri May 06 2016 Sandro Mani <manisandro@gmail.com>- 2.1.0-4
- Enable libKML support
  Resolves: #1332008

* Tue May 03 2016 Adam Williamson <awilliam@redhat.com> - 2.1.0-3
- rebuild for updated poppler

* Tue May  3 2016 Marek Kasik <mkasik@redhat.com> - 2.1.0-2
- Rebuild for poppler-0.43.0

* Mon May 02 2016 Jozef Mlich <imlich@fit.vutbr.cz> - 2.1.0-1
- New upstream release

* Mon Apr 18 2016 Tom Hughes <tom@compton.nu> - 2.0.2-5
- Rebuild for libdap change Resoloves: #1328104

* Tue Feb 16 2016 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.2-4
- Add Python 3 support

* Sun Feb 14 2016 Volker Froehlich <volker27@gmx.at> - 2.0.2-3
- Add patch for GDAL issue #6360

* Mon Feb 08 2016 Volker Froehlich <volker27@gmx.at> - 2.0.2-2
- Rebuild for armadillo 6

* Thu Feb 04 2016 Volker Froehlich <volker27@gmx.at> - 2.0.2-1
- New upstream release
- Fix geos support (BZ #1284714)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Marek Kasik <mkasik@redhat.com> 2.0.1-5
- Rebuild for poppler-0.40.0

* Fri Jan 15 2016 Adam Jackson <ajax@redhat.com> 2.0.1-4
- Rebuild for libdap soname bump

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-3
- Rebuilt for libwebp soname bump

* Sun Oct 18 2015 Volker Froehlich <volker27@gmx.at> - 2.0.1-2
- Solve BZ #1271906 (Build iso8211 and s57 utilities)

* Thu Sep 24 2015 Volker Froehlich <volker27@gmx.at> - 2.0.1-1
- Updated for 2.0.1; Add Perl module manpage

* Wed Sep 23 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-5
- Rebuild for libdap 3.15.1

* Sun Sep 20 2015 Volker Froehlich <volker27@gmx.at> - 2.0.0-4
- Support openjpeg2

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2.0.0-3
- Rebuilt for Boost 1.59

* Sun Aug 09 2015 Jonathan Wakely <jwakely@redhat.com> 2.0.0-2
- Patch to set _XOPEN_SOURCE correctly (bug #1249703)

* Sun Jul 26 2015 Volker Froehlich <volker27@gmx.at> - 2.0.0-1
- Disable charls support due to build issues
- Solve a string formatting and comment errors in the Perl swig template

* Wed Jul 22 2015 Marek Kasik <mkasik@redhat.com> - 1.11.2-12
- Rebuild (poppler-0.34.0)

* Fri Jul  3 2015 José Matos <jamatos@fedoraproject.org> - 1.11.2-11
- Rebuild for armadillo 5(.xxx.y)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Volker Fröhlich <volker27@gmx.at> - 1.11.2-9
- Rebuild for Perl's dropped module_compat_5.20.*

* Tue Jun 09 2015 Dan Horák <dan[at]danny.cz> - 1.11.2-8
- add upstream patch for poppler >= 31

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.11.2-7
- Perl 5.22 rebuild

* Thu May 21 2015 Devrim Gündüz <devrim@gunduz.org> - 1.11.2-6
- Fix proj soname in ogr/ogrct.cpp. Patch from Sandro Mani
  <manisandro @ gmail.com>  Fixes #1212215.

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.11.2-5
- Rebuild for hdf5 1.8.15

* Sat Apr 18 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.11.2-4
- Rebuild for gcc-5.0.1 ABI changes.

* Tue Mar 31 2015 Orion Poplawski <orion@cora.nwra.com> - 1.11.2-3
- Rebuild for g2clib fix

* Wed Mar 11 2015 Devrim Gündüz <devrim@gunduz.org> - 1.11.2-2
- Rebuilt for proj 4.9.1

* Tue Feb 17 2015 Volker Fröhlich <volker27@gmx.at> - 1.11.2-1
- New release
- Remove obsolete sqlite patch

* Fri Jan 23 2015 Marek Kasik <mkasik@redhat.com> - 1.11.1-6
- Rebuild (poppler-0.30.0)

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 1.11.1-5
- Rebuild for hdf5 1.8.4

* Sat Dec  6 2014 Volker Fröhlich <volker27@gmx.at> - 1.11.1-4
- Apply upstream changeset 27949 to prevent a crash when using sqlite 3.8.7

* Tue Dec  2 2014 Jerry James <loganjerry@gmail.com> - 1.11.1-3
- Don't try to install perllocal.pod (bz 1161231)

* Thu Nov 27 2014 Marek Kasik <mkasik@redhat.com> - 1.11.1-3
- Rebuild (poppler-0.28.1)

* Fri Nov 14 2014 Dan Horák <dan[at]danny.cz> - 1.11.1-2
- update gdal-config for ppc64le

* Thu Oct  2 2014 Volker Fröhlich <volker27@gmx.at> - 1.11.1-1
- New release
- Correct test suite source URL

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11.0-9
- Perl 5.20 rebuild

* Mon Aug 25 2014 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-7
- Rebuilt for libgeotiff

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Volker Fröhlich <volker27@gmx.at> - 1.11.0-6
- Add aarch64 to gdal-config script (BZ#1129295)

* Fri Jul 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.11.0-5
- rebuild (libspatialite)

* Mon Jul 14 2014 Orion Poplawski <orion@cora.nwra.com> - 1.11.0-4
- Rebuild for libgeotiff 1.4.0

* Fri Jul 11 2014 Orion Poplawski <orion@cora.nwra.com> - 1.11.0-3
- Rebuild for libdap 3.13.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Volker Fröhlich <volker27@gmx.at> - 1.11.0-1
- New upstream release
- Remove libgcj as BR, as it no longer exists in F21
- Re-enable ogdi and spatialite where possible
- Adapt Python-BR to python2-devel
- Obsolete Ruby bindings, due to the suggestion of Even Rouault
- Preserve timestamp of Fedora README file
- Explicitly create HTML documentation with Doxygen
- Make test execution conditional
- Truncate changelog

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.10.1-6
- Use Requires: java-headless rebuild (#1067528)

* Fri Jan 10 2014 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-5
- Rebuild for armadillo soname bump

* Wed Jan 08 2014 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-4
- Rebuild for cfitsio 3.360

* Thu Jan 02 2014 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-3
- Rebuild for libwebp soname bump

* Sat Sep 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-2
- Rebuild to pick up atlas 3.10 changes

* Sun Sep  8 2013 Volker Fröhlich <volker27@gmx.at> - 1.10.1-1
- New upstream release

* Fri Aug 23 2013 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-1
- Update to 1.10.0
- Enable PCRE support
- Drop man patch applied upstream
- Drop dods patch fixed upstream
- Add more tex BRs to handle changes in texlive packaging
- Fix man page install location

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 1.9.2-12
- Rebuild (poppler-0.24.0)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.9.2-10
- Perl 5.18 rebuild

* Thu Jul 11 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.2-9
- Rebuild for cfitsio 3.350

* Mon Jun 24 2013 Volker Fröhlich <volker27@gmx.at> - 1.9.2-8
- Rebuild for poppler 0.22.5

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.2-7
- Update Java/JNI for new guidelines, also fixes bug #908065

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.2-6
- Rebuild for hdf5 1.8.11

* Mon Apr 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.2-5
- Rebuild for ARM libspatialite issue

* Tue Mar 26 2013 Volker Fröhlich <volker27@gmx.at> - 1.9.2-4
- Rebuild for cfitsio 3.340

* Sun Mar 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.2-3
- rebuild (libcfitsio)

* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Sun Mar 10 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.2-1
- Update to 1.9.2
- Drop poppler and java-swig patches applied upstream

* Fri Jan 25 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.9.1-18
- Rebuild with geos 3.3.7.

* Mon Jan 21 2013 Volker Fröhlich <volker27@gmx.at> - 1.9.1-17
- Rebuild due to libpoppler 0.22

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.9.1-16
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-15
- Rebuild, see
  http://lists.fedoraproject.org/pipermail/devel/2012-December/175685.html

* Thu Dec 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.1-14
- Tweak -fpic CFLAGS to fix FTBFS on ARM

* Mon Dec  3 2012 Orion Poplawski <orion@cora.nwra.com> - 1.9.1-13
- Rebuild for hdf5 1.8.10

* Sun Dec  2 2012 Bruno Wolff III <bruno@wolff.to> - 1.9.1-12
- Rebuild for libspatialite soname bump

* Thu Aug  9 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.1-11
- Correct and extend conditionals for ppc andd ppc64, considering libspatialite
  Related to BZ #846301

* Sun Jul 29 2012 José Matos <jamatos@fedoraproject.org> - 1.9.1-10
- Use the correct shell idiom "if true" instead of "if 1"

* Sun Jul 29 2012 José Matos <jamatos@fedoraproject.org> - 1.9.1-9
- Ignore for the moment the test for armadillo (to be removed after gcc 4.7.2 release)

* Fri Jul 27 2012 José Matos <jamatos@fedoraproject.org> - 1.9.1-8
- Rebuild for new armadillo

* Fri Jul 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.1-7
- Build with PIC

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-5
- Perl 5.16 rebuild

* Sat Jul  7 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.1-4
- Delete unnecessary manpage, that seems to be created with
  new Doxygen (1.8.1 or 1.8.1.1)

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 1.9.1-3
- Rebuild (poppler-0.20.1)

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-2
- Perl 5.16 rebuild

* Wed May 23 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.1-1
- New upstream release
- Update poppler patch
- Add cleaner script

* Sun May 20 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.0-5
- Patches for libpoppler 0.20, libdap 3.11.3 and swig 2.0.6

* Thu May 10 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.0-4
- Correct provides-filtering as of https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Usage
- Support webp
- Remove bogus libjpeg-turbo conditional
- Update Ruby ABI version to 1.9.1
- Install Ruby bindings to vendorarchdir on F17 and later
- Conditionals for Ruby specific elements for versions prior F17 and for EPEL
- Correct quotes for CFLAGS and Ruby
- Disable ogdi, until BZ#816282 is resolved

* Wed Apr 25 2012 Orion Poplawski <orion@cora.nwra.com> - 1.9.0-2
- Rebuild for cfitsio 3.300

* Sun Feb 26 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.0-1
- Completely re-work the original spec-file
  The major changes are:
- Add a libs sub-package
- Move Python scripts to python sub-package
- Install the documentation in a better way and with less slack
- jar's filename is versionless
- Update the version in the Maven pom automatically
- Add a plugins directory
- Add javadoc package and make the man sub-package noarch
- Support many additional formats
- Drop static sub-package as no other package uses it as BR
- Delete included libs before building
- Drop all patches, switch to a patch for the manpages, patch for JAVA path
- Harmonize the use of buildroot and RPM_BUILD_ROOT
- Introduce testversion macro

* Sun Feb 19 2012 Volker Fröhlich <volker27@gmx.at> - 1.7.3-14
- Require Ruby abi
- Add patch for Ruby 1.9 include dir, back-ported from GDAL 1.9
- Change version string for gdal-config from <version>-fedora to
  <version>
- Revert installation path for Ruby modules, as it proofed wrong
- Use libjpeg-turbo

* Thu Feb  9 2012 Volker Fröhlich <volker27@gmx.at> - 1.7.3-13
- Rebuild for Ruby 1.9
  http://lists.fedoraproject.org/pipermail/ruby-sig/2012-January/000805.html

* Tue Jan 10 2012 Volker Fröhlich <volker27@gmx.at> - 1.7.3-12
- Remove FC10 specific patch0
- Versioned MODULE_COMPAT_ Requires for Perl (BZ 768265)
- Add isa macro to base package Requires
- Remove conditional for xerces_c in EL6, as EL6 has xerces_c
  even for ppc64 via EPEL
- Remove EL4 conditionals
- Replace the python_lib macro definition and install Python bindings
  to sitearch directory, where they belong
- Use correct dap library names for linking
- Correct Ruby installation path in the Makefile instead of moving it later
- Use libdir variable in ppc64 Python path
- Delete obsolete chmod for Python libraries
- Move correction for Doxygen footer to prep section
- Delete bundled libraries before building
- Build without bsb and remove it from the tarball
- Use mavenpomdir macro and be a bit more precise on manpages in
  the files section
- Remove elements for grass support --> Will be replaced by plug-in
- Remove unnecessary defattr
- Correct version number in POM
- Allow for libpng 1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.7.3-11
- Rebuild for new libpng

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 1.7.3-10
- Rebuild for hdf5 1.8.7

* Fri Apr 22 2011 Volker Fröhlich <volker27@gmx.at> - 1.7.3-9
- Patched spaces problem for Mapinfo files (mif)
  (http://trac.osgeo.org/gdal/ticket/3694)
- Replaced all define macros with global
- Corrected ruby_sitelib to ruby_sitearch
- Use python_lib and ruby_sitearch instead of generating lists
- Added man-pages for binaries
- Replaced mkdir and install macros
- Removed Python files from main package files section, that
  effectively already belonged to the Python sub-package

* Mon Apr 11 2011 Volker Fröhlich <volker27@gmx.at> - 1.7.3-8
- Solved image path problem with Latex
- Removed with-tiff and updated with-sqlite to with-sqlite3
- Add more refman documents
- Adapted refman loop to actual directories
- Harmonized buildroot macro use

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 1.7.3-7
- Rebuild for netcdf 4.1.2

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.7.3-6
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Sun Mar 20 2011 Volker Fröhlich <volker27@gmx.at> - 1.7.3-5
- Dropped unnecessary encoding conversion for Russian refman
- Install Russian refman
- Don't try to install refman for sdts and dgn, as they fail to compile
- Added -p to post and postun
- Remove private-shared-object-provides for Python and Perl
- Remove installdox scripts
- gcc 4.6 doesn't accept -Xcompiler

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.3-4
- Rebuilt with xerces-c 3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Viji Nair <viji [AT] fedoraproject DOT org> - 1.7.3-2
- Install all the generated pdf documentation.
- Build documentation as a separate package.
- Spec cleanup

* Fri Nov 19 2010 Viji Nair <viji [AT] fedoraproject DOT org> - 1.7.3-1
- Update to latest upstream version
- Added jnis
- Patches updated with proper version info
- Added suggestions from Ralph Apel <r.apel@r-apel.de>
	+ Versionless symlink for gdal.jar
	+ Maven2 pom
	+ JPP-style depmap
	+ Use -f XX.files for ruby and python
