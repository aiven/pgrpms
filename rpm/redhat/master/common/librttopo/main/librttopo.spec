%pgdg_set_gis_variables

Name:		librttopo
Version:	1.1.0
Release:	1%{?dist}
Summary:	Create and manage SQL/MM topologies

License:	GPLv2+
URL:		https://git.osgeo.org/gitea/rttopo/%{name}
Source0:	https://git.osgeo.org/gitea/rttopo/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires:	autoconf automake gcc libtool make
BuildRequires:	pgdg-srpm-macros >= 1.0.12
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}

%description
The RT Topology Library exposes an API to create and manage standard
(ISO 13249 aka SQL/MM) topologies using user-provided data stores.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}

%build
CFLAGS="$CFLAGS -I%{geosinstdir}/include -fPIE"; export CFLAGS
autoreconf -ifv
export PATH=%{geosinstdir}/bin:$PATH
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%license COPYING
%doc CREDITS NEWS.md README.md TODO
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}.so

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}_geom.h
%{_libdir}/pkgconfig/rttopo.pc

%changelog
* Mon Feb 15 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  libspatialite50 packaging, per Fedora spec file written by
  Sandro Mani (ours is a bir different then that spec file).
