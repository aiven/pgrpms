%global sname pgespresso

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Optional Extension for Barman
Name:		%{sname}%{pgmajorversion}
Version:	1.2
Release:	1%{?dist}.1
License:	PostgreSQL
Source0:	https://github.com/2ndquadrant-it/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/2ndquadrant-it/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description

pgespresso is an extension that adds functions and views to be used by Barman,
the disaster recovery tool written by 2ndQuadrant and released as open source
(http://www.pgbarman.org/). Requires at least Barman 1.3.1 and PostgreSQL 9.2.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

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

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install  README file under PostgreSQL installation directory:
%{__install}  -d %{buildroot}%{pginstdir}/share/extension
%{__install}  -m 755 README.asciidoc  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.asciidoc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.asciidoc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 9 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Sun May 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Tue Apr 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-2
- Remove barman dependency

* Mon Apr 14 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
