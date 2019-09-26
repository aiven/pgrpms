%global postgisminmajorversion 2.2
%global osmpgroutingmajorversion 2.3
%global sname	osm2pgrouting

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Import tool for OpenStreetMap data to pgRouting database
Name:		%{sname}_%{pgmajorversion}
Version:	%{osmpgroutingmajorversion}.6
Release:	1%{dist}.1
License:	GPLv2
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/pgRouting/%{sname}/
BuildRequires:	gcc-c++ libpqxx-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 2.8.8
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel, expat-devel
BuildRequires:	boost-devel >= 1.53 postgis
Requires:	postgis2_%{pgmajorversion} >= %{postgisminmajorversion}
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
Import tool for OpenStreetMap data to pgRouting database.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
#install -d build
#cd build
%if 0%{?rhel} && 0%{?rhel} == 7
cmake3 .. \
%else
%cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_INCLUDE_DIR:PATH=%{pginstdir}/include \
	-DPOSTGRESQL_LIBRARIES:PATH=%{pginstdir}/lib/libpq.so.5 \
	-DCMAKE_BUILD_TYPE=Release \
	-H. -Bbuild

cd build/
%{__make}
%install
%{__rm} -rf %{buildroot}

%{__make} -C build install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{_datadir}/%{sname}/Readme.md
%doc %{_datadir}/%{sname}/COPYING
%else
%doc %{_datadir}/%{sname}/Readme.md
%license %{_datadir}/%{sname}/COPYING
%endif
%attr (755,root,root) %{_bindir}/%{sname}
%dir %{_datadir}/%{sname}/
%{_datadir}/%{sname}/mapconfig.xml
%{_datadir}/%{sname}/mapconfig_for_bicycles.xml
%{_datadir}/%{sname}/mapconfig_for_cars.xml
%{_datadir}/%{sname}/mapconfig_for_pedestrian.xml

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3.6-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> 2.3.6-1
- Update to 2.3.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.5-1.1
- Rebuild against PostgreSQL 11.0

* Sun Jul 1 2018 Devrim Gündüz <devrim@gunduz.org> 2.3.5-1
- Update to 2.3.5

* Wed Dec 20 2017 Devrim Gündüz <devrim@gunduz.org> 2.3.3-1
- Update to 2.3.3

* Sat Oct 14 2017 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PostgreSQL RPM repository.
