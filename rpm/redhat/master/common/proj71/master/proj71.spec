%global sname proj

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global sqlitepname	sqlite33
%global sqlite33dir	/usr/sqlite330
%else
%global sqlitepname	sqlite
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

%pgdg_set_gis_variables

Name:		%{sname}71
Version:	7.1.0
Release:	1%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	%{sqlitepname}-devel >= 3.7 gcc-c++ libcurl-devel
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.4

%if 0%{?fedora} > 29 || 0%{?rhel} == 8
Requires:	%{sqlitepname}-libs >= 3.7
%else
Requires:	%{sqlitepname}
%endif

Obsoletes:	proj70 <= 7.0.2 proj63 <= 6.3.1 proj62 <= 6.2.1
Provides:	proj70 <= 7.0.2 proj63 <= 6.3.1 proj62 <= 6.2.1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

Obsoletes:	proj70-devel <= 7.0.2 proj63-devel <= 6.3.1 proj62-devel <= 6.2.1
Provides:	proj70-devel <= 7.0.2 proj63-devel <= 6.3.1 proj62-devel <= 6.2.1


%package static
Summary:	Development files for PROJ
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

Obsoletes:	proj70-static <= 7.0.2 proj63-static <= 6.3.1 proj62-static <= 6.2.1
Provides:	proj70-static <= 7.0.2 proj63-static <= 6.3.1 proj62-static <= 6.2.1

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions. Proj docs: http://www.remotesensing.org/dl/new_docs/

%description devel
This package contains libproj and the appropriate header files and man pages.

%description static
This package contains libproj static library.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib" ; export SHLIB_LINK

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export SQLITE3_CFLAGS="-I%{sqlite33dir}/include"
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

./configure --prefix=%{projinstdir} --with-curl

%{__make} %{?_smp_mflags}

%install
%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

%{__rm} -rf %{buildroot}
%make_install
%{__install} -d %{buildroot}%{projinstdir}/share/%{sname}
%{__install} -d %{buildroot}%{projinstdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{projinstdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%clean
%{__rm} -rf %{buildroot}

%post
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%postun
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc %{projinstdir}/share/doc/*
%{projinstdir}/bin/*
%{projinstdir}/share/man/man1/*.1
%{projinstdir}/share/proj/*
%{projinstdir}/lib/libproj.so.19*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{projinstdir}/share/man/man1/*.1
%{projinstdir}/include/*.h
%{projinstdir}/include/proj/*
%{projinstdir}/lib/*.so
%{projinstdir}/lib/*.a
%attr(0755,root,root) %{projinstdir}/lib/pkgconfig/%{sname}.pc
%exclude %{projinstdir}/lib/libproj.a
%exclude %{projinstdir}/lib/libproj.la
%{projinstdir}/include/proj/util.hpp

%files static
%defattr(-,root,root,-)
%{projinstdir}/lib/libproj.a
%{projinstdir}/lib/libproj.la

%changelog
* Mon Aug 17 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.1.0-1
- Initial 7.1 packaging for PostgreSQL RPM Repository, using the
  7.0 spec file.
