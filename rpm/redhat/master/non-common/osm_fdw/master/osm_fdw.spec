%global debug_package %{nil}
%global sname osm_fdw

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL foreign data wrapper OSM PBF
Name:		%{sname}%{pgmajorversion}
Version:	4.0.0
Release:	1%{?dist}
License:	BSD
Source0:	https://api.pgxn.org/dist/osm_fdw/%{version}/osm_fdw-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
Patch1:		%{sname}-missinginclude.patch
URL:		https://github.com/vpikulik/postgres_osm_pbf_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel protobuf-c-devel
Requires:	postgresql%{pgmajorversion}-server, protobuf-c

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with osm.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

strip %{buildroot}%{pginstdir}/lib/*.so

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%attr(755,root,root) %{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/%{sname}/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/osm_reader/*.bc
  %endif
 %endif
%endif

%changelog
* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
