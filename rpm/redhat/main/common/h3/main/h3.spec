%global _vpath_builddir .
%global sname	h3

Summary:	A Hexagonal Hierarchical Geospatial Indexing System
Name:		%{sname}
Version:	4.1.0
Release:	2PGDG%{dist}
License:	Apache
Source0:	https://github.com/uber/h3/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/uber/h3
BuildRequires:	gcc cmake libtool

%description
H3 is a geospatial indexing system using a hexagonal grid that can be
(approximately) subdivided into finer and finer hexagonal grids,
combining the benefits of a hexagonal grid with S2's hierarchical
subdivisions.

Documentation is available at https://h3geo.org

%package devel
Summary:	H3 development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for h3.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Release \
	-DBUILD_SHARED_LIBS:BOOL=ON  ..
%else
%cmake3 -DCMAKE_BUILD_TYPE=Release ..
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd
%{__mv} %{buildroot}/%{_includedir}/h3/h3api.h %{buildroot}/%{_includedir}/

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%{_bindir}/cellToBoundary
%{_bindir}/cellToBoundaryHier
%{_bindir}/cellToLatLng
%{_bindir}/cellToLatLngHier
%{_bindir}/cellToLocalIj
%{_bindir}/gridDisk
%{_bindir}/gridDiskUnsafe
%{_bindir}/h3
%{_bindir}/h3ToComponents
%{_bindir}/h3ToHier
%{_bindir}/latLngToCell
%{_bindir}/localIjToCell
/usr/lib/libh3.so*

%files devel
%{_includedir}/h3api.h
/usr/lib/cmake/%{sname}/*.cmake

%changelog
* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2PGDG
- Fix SLES-15 builds

* Sat Nov 4 2023 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
- Initial packaging of H3 to support h3-pg extension.
