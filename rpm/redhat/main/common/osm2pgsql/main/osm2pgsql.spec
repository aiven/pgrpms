%global sname osm2pgsql

%pgdg_set_gis_variables

%global projmajorversion %proj92majorversion
%global projfullversion %proj92fullversion
%global projinstdir %proj92instdir

Summary:	Import map data from OpenStreetMap to a PostgreSQL database
Name:		%{sname}
Version:	1.9.2
Release:	1PGDG%{?dist}
License:	GPLv2
Source0:	https://github.com/%{sname}-dev/%{sname}/archive/refs/tags/1.9.2.tar.gz
URL:		https://github.com/%{sname}-dev/%{sname}

BuildRequires:	make gcc-c++ cmake libtool boost-devel bzip2-devel
BuildRequires:	catch2-devel catch2-static clang-tools-extra
BuildRequires:	expat-devel fmt-devel json-devel libosmium-devel libxml2-devel
BuildRequires:	lua-devel
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion}
BuildRequires:	protozero-devel protozero-static zlib-devel
BuildRequires:	python3-devel python3-behave python3-osmium
BuildRequires:	python3-psycopg2
BuildRequires:	libpq5-devel

Requires:	libpq5

%description
osm2pgsql is a tool for loading OpenStreetMap data into a PostgreSQL /
PostGIS database suitable for applications like rendering into a map,
geocoding with Nominatim, or general analysis.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake .. \
%else
%cmake3 .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=Release \
	-DPROJ_LIBRARY=%{projinstdir}/lib64/libproj.so \
	-DPROJ6_INCLUDE_DIR=%{projinstdir}/include \
	-DEXTERNAL_FMT=ON \
	-DEXTERNAL_LIBOSMIUM=ON \
	-DEXTERNAL_PROTOZERO=ON \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

popd

%{__make} -C "build/%{_vpath_builddir}" %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} -C "build/%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_bindir}/%{sname}
%{_bindir}/%{sname}-replication
%{_mandir}/man1/%{sname}*
%{_datadir}/%{sname}/*.style

%changelog
* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.9.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
