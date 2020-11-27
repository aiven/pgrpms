%global sname proj
%global proj70instdir /usr/%{sname}70

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global sqlitepname	sqlite33
%global sqlite33dir	/usr/sqlite330
%else
%global sqlitepname	sqlite
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Name:		%{sname}70
Version:	7.0.1
Release:	4%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	%{sqlitepname}-devel >= 3.7 gcc-c++ libcurl-devel
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.9

%if 0%{?fedora} > 29 || 0%{?rhel} == 8
Requires:	%{sqlitepname}-libs >= 3.7
%else
Requires:	%{sqlitepname}
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif


%package static
Summary:	Development files for PROJ
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
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
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
LDFLAGS="-Wl,-rpath,%{proj70instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj70instdir}/lib" ; export SHLIB_LINK

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export SQLITE3_CFLAGS="-I%{sqlite33dir}/include"
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

./configure --prefix=%{proj70instdir} --with-curl

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
%{__install} -d %{buildroot}%{proj70instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj70instdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{proj70instdir}/share/doc/

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
%doc %{proj70instdir}/share/doc/*
%{proj70instdir}/bin/*
%{proj70instdir}/share/man/man1/*.1
%{proj70instdir}/share/proj/*
%{proj70instdir}/lib/libproj.so.19*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj70instdir}/share/man/man1/*.1
%{proj70instdir}/include/*.h
%{proj70instdir}/include/proj/*
%{proj70instdir}/lib/*.so
%{proj70instdir}/lib/*.a
%attr(0755,root,root) %{proj70instdir}/lib/pkgconfig/%{sname}.pc
%exclude %{proj70instdir}/lib/libproj.a
%exclude %{proj70instdir}/lib/libproj.la
%{proj70instdir}/include/proj/util.hpp

%files static
%defattr(-,root,root,-)
%{proj70instdir}/lib/libproj.a
%{proj70instdir}/lib/libproj.la

%changelog
* Fri Nov 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.1-4
- Make sure that each PROJ package will install into their own directory,
  not under the latest one.

* Thu Nov 26 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.1-3
- Stop obsoleting older versions of PROJ. We already fixed issues with other
  packages.

* Sun May 10 2020 John K. Harvey <john.harvey@crunchydata.com> - 0:7.0.1-2
- Add CPPFLAGS for sqlite33dir on EL-7 so that sqlite3.h is picked up
  during compilation.

* Mon May 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.1-1
- Update to 7.0.1
- Obsolete older Proj installations to avoid linking issues with packages
  depends on Proj.

* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.0-3
- Fix CentOS 7 and CentOS 8 builds, per mock build testing by Talha.
- Switch to pgdg-srpm-macros

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.0-2
- Relax pkgconfig patch to avoid aclocal calls. Per discussion
  with upstream

* Fri Mar 13 2020 Devrim Gündüz <devrim@gunduz.org> - 0:7.0.0-1
- Initial 7.0 packaging for PostgreSQL RPM Repository
- Build with curl support
- Add a patch to fix SLES 12 and  RHEL 7 builds, per
  https://github.com/OSGeo/PROJ/issues/2062
- Backport a 7.0.1 patch to fix pkgconfig file:
  https://github.com/OSGeo/PROJ/issues/2070
