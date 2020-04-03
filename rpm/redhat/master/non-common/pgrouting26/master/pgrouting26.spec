%global postgismajorversion 2.5
%global pgroutingmajorversion 2.6
%global sname	pgrouting

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.3
Release:	1%{dist}
License:	GPLv2
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		http://pgrouting.org/
BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake => 2.8.8
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	boost-devel >= 1.53, CGAL-devel => 4.4, gmp-devel
Requires:	postgis25_%{pgmajorversion} >= %{postgismajorversion}
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pgRouting extends the PostGIS / PostgreSQL geospatial database to
provide geospatial routing functionality.

Advantages of the database routing approach are:

- Data and attributes can be modified by many clients, like QGIS and
uDig through JDBC, ODBC, or directly using Pl/pgSQL. The clients can
either be PCs or mobile devices)
- Data changes can be reflected instantaneously through the routing
engine. There is no need for precalculation.
- The “cost” parameter can be dynamically calculated through SQL and its
value can come from multiple fields or tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
install -d build
cd build
%if 0%{?rhel} && 0%{?rhel} == 7
cmake3 .. \
%else
%cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_BIN=%{pginstdir}/bin \
	-DCMAKE_BUILD_TYPE=Release \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} -C build install \
	DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md BOOST_LICENSE_1_0.txt
%attr(755,root,root) %{pginstdir}/lib/libpgrouting-%{pgroutingmajorversion}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6.3-1
- Update to 2.6.3
- Update PostGIS version to 2.5, and update dependency to match
  the PostGIS version numbering.

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6.2-1
- Update to 2.6.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1.1
- Rebuild against PostgreSQL 11.0

* Mon Sep 24 2018 Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1

* Wed Mar 21 2018 Devrim Gündüz <devrim@gunduz.org> 2.6.0-1
- Release 2.6.0
