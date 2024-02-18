%global sname osm2pgsql

%pgdg_set_gis_variables

%global projmajorversion %proj93majorversion
%global projfullversion %proj93fullversion
%global projinstdir %proj93instdir

Summary:	Import map data from OpenStreetMap to a PostgreSQL database
Name:		%{sname}
Version:	1.11.0
Release:	1PGDG%{?dist}
License:	GPLv2
Source0:	https://github.com/%{sname}-dev/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/%{sname}-dev/%{sname}

BuildRequires:	make gcc-c++ cmake libtool libpq5-devel libosmium-devel >= 2.20.0-42
BuildRequires:	libxml2-devel proj%{projmajorversion}-devel >= %{projfullversion}
BuildRequires:	protozero-devel python3-psycopg2 python3-devel
BuildRequires:	zlib-devel

%if 0%{?suse_version} >= 1500
BuildRequires:	libboost_headers1_66_0-devel libbz2-devel
BuildRequires:	Catch2-2-devel clang-tools
BuildRequires:	libexpat-devel fmt-devel nlohmann_json-devel
BuildRequires:	lua54-devel python3-behave
%else
BuildRequires:	boost-devel bzip2-devel
BuildRequires:	catch2-devel clang-tools-extra
BuildRequires:	expat-devel fmt-devel json-devel
BuildRequires:	lua-devel python3-behave
%endif

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
%defattr(755,root,root,755)
%{_bindir}/%{sname}
%{_bindir}/%{sname}-replication
%{_mandir}/man1/%{sname}*
%{_datadir}/%{sname}/*.style

%changelog
* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-1PGDG
- Update to 1.11.0
- Build against Proj 9.3.1
- Add SLES 15 support

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.10.0-1PGDG
- Update to 1.10.0

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.9.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
