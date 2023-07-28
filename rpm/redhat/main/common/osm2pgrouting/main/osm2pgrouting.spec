%global sname	osm2pgrouting

Summary:	Import tool for OpenStreetMap data to pgRouting database
Name:		%{sname}
Version:	2.3.8
Release:	4PGDG%{dist}
License:	GPLv2
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/pgRouting/%{sname}/
BuildRequires:	gcc-c++ libpqxx-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 2.8.8
%endif
BuildRequires:	libpq5-devel, expat-devel
BuildRequires:	boost-devel >= 1.53 pgdg-srpm-macros
Requires:	libpqxx boost-program-options
Requires:	libpq5

Obsoletes:	%{sname}_15 <= 2.3.8
Obsoletes:	%{sname}_14 <= 2.3.8
Obsoletes:	%{sname}_13 <= 2.3.8
Obsoletes:	%{sname}_12 <= 2.3.8
Obsoletes:	%{sname}_11 <= 2.3.8

%description
Import tool for OpenStreetMap data to pgRouting database.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
cmake3 .. \
%else
%cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_INCLUDE_DIR:PATH=%{_includedir} \
	-DPOSTGRESQL_LIBRARIES:PATH=%{_libdir}/libpq.so.5 \
	-DCMAKE_BUILD_TYPE=Release \
	-H. -Bbuild

cd build/
%{__make}

%install
%{__rm} -rf %{buildroot}

%{__make} -C build install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post	-p %{_sbindir}/ldconfig
%postun	-p %{_sbindir}/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_datadir}/%{sname}/README.md
%license %{_datadir}/%{sname}/COPYING
%attr (755,root,root) %{_bindir}/%{sname}
%dir %{_datadir}/%{sname}/
%{_datadir}/%{sname}/mapconfig.xml
%{_datadir}/%{sname}/mapconfig_for_bicycles.xml
%{_datadir}/%{sname}/mapconfig_for_cars.xml
%{_datadir}/%{sname}/mapconfig_for_pedestrian.xml

%changelog
* Fri Jul 28 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.8-4PGDG
- Rebuild against new libpqxx

* Wed Jul 26 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.8-3PGDG
- Depend on common libpq5, not a particular PostgreSQL version.
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3.8-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jun 3 2021 Devrim Gündüz <devrim@gunduz.org> 2.3.8-1
- Update to 2.3.8
- Spec file cleanup

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
