%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		postgresql%{pgmajorversion}-tcl
Version:	2.3.1
Release:	1%{?dist}
Summary:	A Tcl client library for PostgreSQL

Group:		Applications/Databases
URL:		https://github.com/flightaware/Pgtcl
License:	BSD

Source0:	https://github.com/flightaware/Pgtcl/archive/v%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

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
./configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir} \
	--with-postgres-include=%{pginstdir}/include --with-postgres-lib=%{pginstdir}/lib \
	--disable-rpath

%{__make} all

%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}
# we don't really need to ship the .h file
%{__rm} -f %{buildroot}%{_includedir}/libpgtcl.h

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
%{_libdir}/tcl%{tcl_version}/pgtcl2.3/
%{_mandir}/mann/pg*

%changelog
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
