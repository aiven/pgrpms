%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	C++ wrapper library around CGAL for PostGIS
Name:		SFCGAL
%if 0%{?fedora} || 0%{?rhel} >= 8
Version:	1.3.7
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
Version:	1.3.1
%endif
Release:	4%{?dist}
License:	GLPLv2
Source:		https://github.com/Oslandia/%{name}/archive/v%{version}.tar.gz
# Adding patches for CGAL 5.x. Grabbed them from Debian folks
# per  https://github.com/Oslandia/SFCGAL/pull/219
%if 0%{?fedora} >= 32
Patch0:		sfcgal-fix-ftbfs-with-cgal-5.x.patch
Patch1:		sfcgal-config.patch
%endif
URL:		http://sfcgal.org/
%if 0%{?fedora} || 0%{?rhel} >= 8
# We provide these package in our repo
BuildRequires:	CGAL-devel >= 4.14
Requires:	CGAL => 4.14
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	CGAL-devel
Requires:	CGAL
%endif
BuildRequires:	cmake pgdg-srpm-macros
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libboost_date_time1_54_0 libboost_thread1_54_0
BuildRequires:	libboost_system1_54_0 libboost_serialization1_54_0
%endif
%else
BuildRequires:	boost-thread, boost-system, boost-date-time, boost-serialization
%endif
BuildRequires:	mpfr-devel, gmp-devel, gcc-c++
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package libs
Summary:	The shared libraries required for SFCGAL
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description libs
The sfcgal-libs package provides the essential shared libraries for SFCGAL.

%package devel
Summary: The development files for SFCGAL
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for SFCGAL.

%prep
%setup -q
%if 0%{?fedora} >= 32
%patch0 -p0
%patch1 -p0
%endif
%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
%endif
%else
%cmake \
%endif
	-D LIB_INSTALL_DIR=%{_lib} -DBoost_NO_BOOST_CMAKE=BOOL:ON .

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install/fast DESTDIR=%{buildroot}

%post
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%post libs
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
%postun libs
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%files
%doc AUTHORS README.md NEWS
%license LICENSE
%{_bindir}/sfcgal-config

%files devel
%{_includedir}/%{name}/

%files libs
%{_libdir}/libSFCGAL.so*
/usr/lib/libSFCGAL.la

%changelog
* Thu Apr 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-4
- Add two patches for CGAL 5 builds

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-3
- Clarify dependencies on RHEL 8, per Talha Bin Rizwan.
- Depend on pgdg-srpm-macros

* Fri Jul 19 2019 John K. Harvey <john.harvey@crunchydata.com> - 1.3.7-2
- Fix broken macro

* Mon Jun 3 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-1
- Update to 1.3.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1.1
- Rebuild against PostgreSQL 11.0

* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2 to support CGAL >= 4.10.1 on Fedora 26+

* Wed Jul 19 2017 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Also Requires CGAL, per Fahar Abbas (EDB QA)

* Thu Nov 19 2015 Oskari Saarenmaa <os@ohmu.fi> 1.2.2-1
- Update to 1.2.2 to support newer CGAL versions

* Fri Oct 30 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial build for PostgreSQL YUM Repository.
