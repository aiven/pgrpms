%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		postgresql%{pgmajorversion}-tcl
Version:	2.1.1
Release:	1%{?dist}
Summary:	A Tcl client library for PostgreSQL

Group:		Applications/Databases
URL:		http://sourceforge.net/projects/pgtclng/
License:	PostgreSQL

Source0:	http://downloads.sourceforge.net/pgtclng/pgtcl%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/pgtclng/Manual/20140912/pgtcldocs-20140912.zip

Patch1:		postgresql-tcl-no-rpath.patch

Provides:	pgtcl = %{version}-%{release}
# pgtcl was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  The cutoff EVR was
# chosen to be later than anything we are likely to ship in Fedora 12.
Provides:	postgresql%{pgmajorversion}-tcl = 8.5.0-1
Obsoletes:	postgresql-tcl < 8.5

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
%setup -q -n pgtcl%{version}

unzip %{SOURCE1}
PGTCLDOCDIR=`basename %{SOURCE1} .zip`
%{__mv} $PGTCLDOCDIR Pgtcl-docs

%patch1 -p1

autoconf

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
./configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir} --with-postgres-include=%{pginstdir}/include --with-postgres-lib=%{pginstdir}/lib

# note: as of pgtcl 1.5.2, its makefile is not parallel-safe
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
%doc Pgtcl-docs/*
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{_libdir}/tcl%{tcl_version}/pgtcl%{version}/

%changelog
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
