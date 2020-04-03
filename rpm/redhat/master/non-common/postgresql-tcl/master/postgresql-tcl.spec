%global _build_id_links none

%global debug_package %{nil}
%global pgtclmajorversion 2.4
%global pgtclprefix /usr/pgtcl%{pgtclmajorversion}

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		postgresql%{pgmajorversion}-tcl
Version:	%{pgtclmajorversion}.0
Release:	2%{?dist}.2
Summary:	A Tcl client library for PostgreSQL

URL:		https://github.com/flightaware/Pgtcl
License:	BSD

Source0:	https://github.com/flightaware/Pgtcl/archive/v%{version}.tar.gz


Requires:	tcl(abi) >= 8.5

BuildRequires:	postgresql%{pgmajorversion}-devel tcl-devel
BuildRequires:	autoconf

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%description
PostgreSQL is an advanced Object-Relational database management system.
The tcl-pgtcl package contains Pgtcl, a Tcl client library for connecting
to a PostgreSQL server.

%prep
%setup -q -n Pgtcl-%{version}

autoconf

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
./configure --prefix=%{pgtclprefix}-%{pgmajorversion} --libdir=%{pgtclprefix}-%{pgmajorversion}/lib --with-tcl=%{_libdir} \
	--with-postgres-include=%{pginstdir}/include --with-postgres-lib=%{pginstdir}/lib \
	--disable-rpath

%{__make} all

%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}
# we don't really need to ship the .h file
%{__rm} -f %{buildroot}%{pgtclprefix}-%{pgmajorversion}/include/pgtclId.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%dir %{pgtclprefix}-%{pgmajorversion}/
%dir %{pgtclprefix}-%{pgmajorversion}/share/man/mann/
%{pgtclprefix}-%{pgmajorversion}/lib/libpgtcl.so
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/libpgtcl%{pgtclmajorversion}.0.so
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/pkgIndex.tcl
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/postgres-helpers.tcl
%{pgtclprefix}-%{pgmajorversion}/share/man/mann/*

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 1 2018 Devrim Gündüz <devrim@gunduz.org> 2.4.0-2
- Apply a workaround for conflicting build-ids.

* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0
- Move files under a new directory. This fixes the parallel
  installation issue (the previous version used to conflict)

* Sun Aug 6 2017 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1, by switching to pgtcl maintained by FlightAware.

* Wed Jan 27 2016 Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Unified spec file for all distros.

* Thu Nov 10 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Use better download URLs.

* Tue Aug 09 2011 Devrim Gunduz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0, per #65.

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0, per:
  http://pgfoundry.org/forum/forum.php?forum_id=1766

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.7.1-1
- Use Fedora's spec for consistency, and update to 1.7.1
- Update spec for 9.0 multiple postmaster support.
