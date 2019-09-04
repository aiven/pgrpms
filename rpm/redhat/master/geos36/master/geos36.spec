%global		sname geos
%global		geosinstdir /usr/%{sname}36

# Specify the subdirectory for the libraries:
%ifarch i686 i386
%global		_geoslibdir lib
%else
%global		_geoslibdir lib64
%endif

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}36
Version:	3.6.3
Release:	1%{?dist}.1
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.bz2
Patch0:		%{name}-gcc43.patch

BuildRequires:	doxygen libtool
BuildRequires:	python-devel
BuildRequires:	gcc-c++

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")


%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Requires:	%{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

%package python
Summary:	Python modules for GEOS
Requires:	%{name} = %{version}-%{release}
BuildRequires:	swig
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description python
Python module to build applications using GEOS and python

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

# fix python path on 64bit
sed -i -e 's|\/lib\/python|$libdir\/python|g' configure
sed -i -e 's|.get_python_lib(0|.get_python_lib(1|g' configure

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

%ifarch ppc64 ppc64le
        export CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=${PPC_MCPU} -mtune=${PPC_MTUNE} -I/opt/%(echo ${PPC_AT})/include"
        export CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=${PPC_MCPU} -mtune=${PPC_MTUNE} -I/opt/%(echo ${PPC_AT})/include"
        export LDFLAGS="-L/opt/%(echo ${PPC_AT})/%{_lib}"
%endif

PYTHON=/usr/bin/python2 ./configure --prefix=%{geosinstdir} --libdir=/usr/geos36/%{_geoslibdir} --disable-static --disable-dependency-tracking --enable-python
# Touch the file, since we are not using ruby bindings anymore:
# Per http://lists.osgeo.org/pipermail/geos-devel/2009-May/004149.html
touch swig/python/geos_wrap.cxx

%{__make} %{?_smp_mflags}

# Make doxygen documentation files
cd doc
%{__make} doxygen-html

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

# Create linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{geosinstdir}/%{_geoslibdir}/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%check
# test module
%{__make} %{?_smp_mflags} check || exit 0

%clean
%{__rm} -rf %{buildroot}

%post
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%else
	/sbin/ldconfig
%endif

%postun
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%else
	/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{geosinstdir}/%{_geoslibdir}/libgeos-%{version}.so
%{geosinstdir}/%{_geoslibdir}/libgeos.so
%{geosinstdir}/%{_geoslibdir}/libgeos_c.so*
%exclude %{geosinstdir}/%{_geoslibdir}/*.a
%exclude %{geosinstdir}/%{_geoslibdir}/*.la
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{geosinstdir}/bin/geos-config
%{geosinstdir}/include/*

%files python
%defattr(-,root,root,-)
%defattr(-,root,root,-)
%dir %exclude %{geosinstdir}/
%dir %{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/
%exclude %{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/_%{sname}.la
%exclude %{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/_%{sname}.a
%{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/_%{sname}.so
%{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}.pth
%{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/%{sname}.py
%{geosinstdir}/%{_geoslibdir}/python%{pyver}/site-packages/%{sname}/%{sname}.py?

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.6.3-1.1
- Rebuild against PostgreSQL 11.0

* Mon Sep 24 2018 Devrim Gündüz <devrim@gunduz.org> - 3.6.3-1
- Update to 3.6.3

* Tue Dec 26 2017 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-3.1
- Remove Source1, and create linker config file manually, so that
  it uses the right path all the time.

* Mon Dec 25 2017 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-3
- Move .so files to main package.

* Thu Nov 23 2017 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-2
- Add a linker config file to satisfy GDAL and other packages
  which we use while building PostGIS.

* Sun Oct 1 2017 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-1
- Initial packaging of 3.6.X for PostgreSQL RPM Repository,
  which is to satisfy PostGIS on older platforms, so that
  users can benefit from all PostGIS features.
