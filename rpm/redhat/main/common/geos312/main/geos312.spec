%global _vpath_builddir .

%global		sname geos
%global		_geosversion	312
%global		geosinstdir /usr/%{sname}%{_geosversion}
%global		_geoslibdir lib64

Name:		%{sname}%{_geosversion}
Version:	3.12.0
Release:	1PGDG%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		https://libgeos.org/
Source0:	http://download.osgeo.org/geos/geos-%{version}.tar.bz2
Patch0:		%{name}-gcc43.patch

%if 0%{?suse_version} && 0%{?suse_version} >= 1499
BuildRequires:	cmake >= 3.13
%else
BuildRequires:	cmake3 >= 3.13
%endif
BuildRequires:	libtool gcc-c++ pgdg-srpm-macros
Provides:	geos%{_geosversion}-python >= %{version}

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Requires:	%{name} = %{version}-%{release}
Obsoletes:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos36 <= 3.6.4 geos37 <= 3.7.3

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
cmake .. -DCMAKE_INSTALL_PREFIX:PATH=/usr \
%endif
%else
%cmake3 .. \
%endif
	-DCMAKE_INSTALL_PREFIX:PATH=%{geosinstdir} -DCMAKE_BUILD_TYPE=Release .. \
	-D LIB_INSTALL_DIR=%{_lib} .

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}

%install
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}

# Remove files we don't ship:
%{__rm} -f %{buildroot}%{geosinstdir}/lib64/cmake/GEOS/geos-config*cmake
%{__rm} -f %{buildroot}%{geosinstdir}/lib64/cmake/GEOS/geos-targets*cmake

# Create linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{geosinstdir}/%{_geoslibdir}/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md
%{geosinstdir}/bin/geosop
%{geosinstdir}/%{_geoslibdir}/libgeos.so.%{version}
%{geosinstdir}/%{_geoslibdir}/libgeos.so
%{geosinstdir}/%{_geoslibdir}/libgeos_c.so*
%if 0%{?rhel} && 0%{?rhel} >= 7
%exclude %{geosinstdir}/%{_geoslibdir}/*.a
%endif
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{geosinstdir}/bin/geos-config
%{geosinstdir}/include/*
%{geosinstdir}/%{_geoslibdir}/pkgconfig/%{sname}.pc

%changelog
* Thu Aug 10 2023 Devrim Gunduz <devrim@gunduz.org> - 3.12.0-1PGDG
- Initial packaging of 3.12.X for the PostgreSQL RPM Repository

