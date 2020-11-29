%global		sname geos
%global		_geosversion	39
%global		geosinstdir /usr/%{sname}%{_geosversion}

%global		_geoslibdir lib64

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Name:		%{sname}%{_geosversion}
Version:	3.9.0
Release:	beta1_1%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}beta1.tar.bz2
Patch0:		%{name}-gcc43.patch

BuildRequires:	doxygen libtool
BuildRequires:	gcc-c++ pgdg-srpm-macros
Obsoletes:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos%{_geosversion}-python >= %{version}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

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
%setup -q -n %{sname}-%{version}beta1
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

# disable internal libtool to avoid hardcoded r-path
%if 0%{?rhel} && 0%{?rhel} >= 7
for makefile in $(find . -type f -name 'Makefile.in'); do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done
%endif

./configure --prefix=%{geosinstdir} --libdir=/usr/geos%{_geosversion}/%{_geoslibdir} --disable-static --disable-dependency-tracking --disable-python

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

%clean
%{__rm} -rf %{buildroot}

%post
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%else
	/sbin/ldconfig
11%endif

%postun
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%else
	/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README.md
%{geosinstdir}/%{_geoslibdir}/libgeos-%{version}.so
%{geosinstdir}/%{_geoslibdir}/libgeos.so
%{geosinstdir}/%{_geoslibdir}/libgeos_c.so*
%if 0%{?rhel} && 0%{?rhel} >= 7
%exclude %{geosinstdir}/%{_geoslibdir}/*.a
%endif
%exclude %{geosinstdir}/%{_geoslibdir}/*.la
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{geosinstdir}/bin/geos-config
%{geosinstdir}/include/*
%{geosinstdir}/%{_geoslibdir}/pkgconfig/%{sname}.pc

%changelog
* Sun Nov 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.9.0beta1
- Initial packaging of 3.9.X for PostgreSQL RPM Repository,
