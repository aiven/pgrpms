# Min dependencies
%global boost_version 1.69
%global qt_version 5.13
%global cmake_version 3.17

# Various variables that defines the release
%global soname 13
%global soversion 14.0.0
%global alphatag %{nil}
%global alphaname %{nil}

Name:		CGAL
Version:	5.0.2
Release:	20%{alphatag}%{?dist}
Summary:	Computational Geometry Algorithms Library

License:	LGPLv3+ and GPLv3+ and Boost
URL:		http://www.cgal.org/
Source0:	https://github.com/CGAL/cgal/releases/download/releases/%{name}-%{version}/%{name}-%{version}.tar.xz
Source10:	CGAL-README.Fedora


# Required devel packages.
BuildRequires:	cmake >= %{cmake_version} gmp-devel boost-devel >= %{boost_version}
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libqt4-devel libqt5-qtbase-common-devel
%endif
%endif

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
BuildRequires:	qt5-devel
%endif

%if 0%{?rhel} && 0%{?rhel} < 8
BuildRequires:	qt3-devel qt-devel >= %{qt_version}
%endif

BuildRequires:	zlib-devel
BuildRequires:	blas-devel lapack-devel mpfr-devel gcc-c++

%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.

%prep
%setup -q -n %{name}-%{version}%{alphaname}

# Fix some file permissions
chmod a-x include/CGAL/export/ImageIO.h
chmod a-x include/CGAL/export/CORE.h
chmod a-x include/CGAL/internal/Static_filters/Equal_3.h
chmod a-x include/CGAL/export/CGAL.h

# Install README.Fedora here, to include it in %%doc
%{__install} -p -m 644 %{SOURCE10} ./README.Fedora

%build

%{__mkdir} build
pushd build
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
%endif
%else
%cmake \
%endif
	-DCGAL_INSTALL_LIB_DIR=%{_lib} -DCGAL_HEADER_ONLY=OFF \
	-DCGAL_INSTALL_DOC_DIR= ${CHANGE_SOVERSION} ..
%{__make} VERBOSE=1 %{?_smp_mflags}
popd


%install
%{__rm} -rf %{buildroot}

pushd build
%{__make} install DESTDIR=$RPM_BUILD_ROOT
popd

# Install demos and examples
%{__mkdir} -p %{buildroot}%{_datadir}/CGAL
touch -r demo %{buildroot}%{_datadir}/CGAL/
%{__cp} -a demo %{buildroot}%{_datadir}/CGAL/demo
%{__cp} -a examples %{buildroot}%{_datadir}/CGAL/examples

%{__rm} -rf %{buildroot}%{_includedir}/CGAL
%{__rm} -rf %{buildroot}%{_libdir}/libCGAL*.so
%{__rm} -rf %{buildroot}%{_libdir}/cmake/CGAL/*
%{__rm} -rf %{buildroot}%{_datadir}/CGAL
%{__rm} -rf %{buildroot}%{_bindir}/*

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL LICENSE.GPL README.Fedora
%{_libdir}/libCGAL.so.%{soname}*
%{_libdir}/libCGAL_Core.so.%{soname}*
%{_libdir}/libCGAL_ImageIO.so.14
%{_libdir}/libCGAL_Qt5.so.14
%{_libdir}/libCGAL_ImageIO.so.14.0.0
%{_libdir}/libCGAL_Qt5.so.14.0.0
%exclude %{_mandir}/man1/cgal_create_cmake_script.1.gz

%changelog
* Thu Apr 23 2020 Devrim Gündüz <devrim@gunduz.org> - 5.0.2-20
- Initial build for PostgreSQL RPM Repository. Fedora 32+ removed
  CGAL main package, so this package only provides that one.
