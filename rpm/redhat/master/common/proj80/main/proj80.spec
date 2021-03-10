%global sname proj

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global sqlitepname	sqlite33
%global sqlite33dir	/usr/sqlite330
%else
%global sqlitepname	sqlite
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%pgdg_set_gis_variables

Name:		%{sname}80
Version:	8.0.0
Release:	1%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	%{sqlitepname}-devel >= 3.7 gcc-c++ libcurl-devel
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.9

%if 0%{?fedora} > 30 || 0%{?rhel} == 8
Requires:	%{sqlitepname}-libs >= 3.7
%else
Requires:	%{sqlitepname}
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%package static
Summary:	Development files for PROJ
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

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
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

LDFLAGS="-Wl,-rpath,%{proj80instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj80instdir}/lib" ; export SHLIB_LINK

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export SQLITE3_CFLAGS="-I%{sqlite33dir}/include"
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

./configure --prefix=%{proj80instdir} --with-curl

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
%{__install} -d %{buildroot}%{proj80instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj80instdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{proj80instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%clean
%{__rm} -rf %{buildroot}

%post
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
%{atpath}/sbin/ldconfig
%endif
%else
/sbin/ldconfig
%endif

%postun
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
%{atpath}/sbin/ldconfig
%endif
%else
/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc %{proj80instdir}/share/doc/*
%{proj80instdir}/bin/*
%{proj80instdir}/share/man/man1/*.1
%{proj80instdir}/share/proj/*
%{proj80instdir}/lib/libproj.so.22*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj80instdir}/share/man/man1/*.1
%{proj80instdir}/include/*.h
%{proj80instdir}/include/proj/*
%{proj80instdir}/lib/*.so
%{proj80instdir}/lib/*.a
%attr(0755,root,root) %{proj80instdir}/lib/pkgconfig/%{sname}.pc
%exclude %{proj80instdir}/lib/libproj.a
%exclude %{proj80instdir}/lib/libproj.la
%{proj80instdir}/include/proj/util.hpp

%files static
%defattr(-,root,root,-)
%{proj80instdir}/lib/libproj.a
%{proj80instdir}/lib/libproj.la

%changelog
* Mon Mar 8 2021 Devrim Gündüz <devrim@gunduz.org> - 0:8.0.0-1
- Initial 8.0 packaging for PostgreSQL RPM Repository.
