%global _vpath_builddir .
%global pgroutingmajorversion 3.1
%global sname	pgrouting

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.0
Release:	3%{dist}
License:	GPLv2
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://pgrouting.org/
BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
# EPEL:
BuildRequires:	boost169-devel
%else
BuildRequires:	cmake => 3.0.0
BuildRequires:	boost-devel >= 1.53
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	gmp-devel
Requires:	postgis >= 2.3

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
pushd build
cmake3 .. \
%if 0%{?rhel} && 0%{?rhel} == 7
	-DBOOST_ROOT=%{_includedir}/boost169 \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_BIN=%{pginstdir}/bin \
	-DCMAKE_BUILD_TYPE=Release \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

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
* Thu Oct 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-3
- Build fixes for Fedora 33

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-2
- Require PostGIS >= 2.3, per Vicky.

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Initial packaging of pgRouting 3.1
