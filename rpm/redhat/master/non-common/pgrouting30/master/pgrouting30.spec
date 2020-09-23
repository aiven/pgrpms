%global postgismajorversion 3.0
%global pgroutingmajorversion 3.0
%global sname	pgrouting

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.2
Release:	1%{dist}
License:	GPLv2
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://pgrouting.org/
BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
# EPEL:
BuildRequires:	boost169-devel
%else
BuildRequires:	cmake => 2.8.8
BuildRequires:	boost-devel >= 1.53
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	gmp-devel
Requires:	postgis30_%{pgmajorversion} >= %{postgismajorversion}
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
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
	%pgdg_set_ppc64le_compiler_flags
%endif

%{__install} -d build
cd build
%if 0%{?rhel} && 0%{?rhel} == 7
cmake3 .. \
	-DBOOST_ROOT=%{_includedir}/boost169 \
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
* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.2-1
- Update to 3.0.2

* Mon Mar 30 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 30 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-rc1.2
- Fix RHEL 7 builds, per tip from Florent Jardin.

* Mon Mar 30 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-rc1.1
- Update to 3.0.0rc1
-
* Fri Oct 25 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-beta-1.1
- Update to 3.0.0beta

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-alpha-1.1
- Initial packaging of pgRouting 3.0
