%global postgismajorversion 2.1
%global pgroutingmajorversion 2.0
%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname	pgrouting

# Add Traveling Salesperson functionality
%{!?tsp_support:%global	tsp_support 1}
# Add Driving Distance functionality
%{!?dd_support:%global	dd_support 1}

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.1
Release:	2%{dist}
License:	GPLv2
Group:		Applications/Databases
Source0:	https://github.com/pgRouting/%{sname}/archive/%{sname}-%{version}.tar.gz
Patch0:		pgrouting-cmake-pgconfig-path.patch
URL:		http://pgrouting.org/
BuildRequires:	gcc-c++, cmake
BuildRequires:	postgresql%{pgmajorversion}-devel, proj-devel, geos-devel
BuildRequires:	boost-devel >= 1.33
%if %{dd_support}
BuildRequires:	CGAL-devel
%endif
Requires:	postgis2_%{pgmajorversion} >= %{postgismajorversion}
Requires:	postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

%setup -q -n %{sname}-%{sname}-%{version}
%patch0 -p0

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if %{tsp_support}
	-DWITH_TSP=ON \
%endif
	-DCMAKE_BUILD_TYPE=Release \
%if %{dd_support}
	-DWITH_DD=ON \
%endif
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

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
%attr(755,root,root) %{pginstdir}/lib/librouting.so
%if %{tsp_support}
%attr(755,root,root) %{pginstdir}/lib/librouting_tsp.so
%endif
%if %{dd_support}
%attr(755,root,root) %{pginstdir}/lib/librouting_dd.so
%endif
%attr(755,root,root) %{pginstdir}/lib/librouting_bd.so
%attr(755,root,root) %{pginstdir}/lib/librouting_ksp.so
%{pginstdir}/share/contrib/pgrouting-%{pgroutingmajorversion}/%{sname}*
%{pginstdir}/share/extension/%{sname}*

%changelog
* Sat Oct 1 2016 Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.1-2
- Rebuilt for CGAL 4.7

* Tue Sep 8 2015 Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Improve description

* Wed Oct 23 2013 Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Mon Sep 2 2013 Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.0-rc1-1
- Update to 2.0.0 rc1
- Remove patch1 -- already in upstream.

* Mon Nov 12 2012 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.5-2
- Add the following features, sponsored by "Norsk institutt for skog og landskap":
 -- Add Traveling Salesperson functionality
 -- Add Driving Distance functionality
- Fix packaging issues, sponsored again by "Norsk institutt for skog og landskap".
- Update URL
- Add a new patch so that pgrouting can find PostgreSQL libs.
- Remove obsoleted patch (pgrouting-pg84.patch) -- already in upstream.
- Add a patch for 9.2, that removes quotes around LANGUAGE 'C'.

* Sat Sep 15 2012 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.5-1
- Update to 1.05

* Wed Jan 20 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.3-5
- Initial import to PostgreSQL RPM repository, with very little cosmetic 
  changes Thanks Peter	for sending spec to me.

* Wed Dec 09 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-4
- New build for PostGIS 1.4.

* Tue May 05 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-3
- Adapted to CentOS 5.

