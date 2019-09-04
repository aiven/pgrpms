%global sname tds_fdw
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	TDS Foreign Data Wrapper for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.8
Release:	1%{?dist}.1
License:	BSD
Source0:	https://github.com/tds-fdw/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/tds-fdw/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel, freetds-devel
Requires:	postgresql%{pgmajorversion}-server, freetds
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This library contains a single PostgreSQL extension, a foreign data wrapper
called "tds_fdw". It can be used to communicate with Microsoft SQL
Server and Sybase databases.

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
%{__make}  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 644 ForeignServerCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignServerCreation-%{sname}.md
install -m 644 ForeignTableCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignTableCreation-%{sname}.md
install -m 644 UserMappingCreation.md %{buildroot}%{pginstdir}/doc/extension/UserMappingCreation-%{sname}.md
install -m 644 Variables.md %{buildroot}%{pginstdir}/doc/extension/Variables-%{sname}.md

%{__rm} -f %{buildroot}/%{_docdir}/pgsql/extension/README.%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1.1
- Rebuild against PostgreSQL 11.0

* Fri Oct 28 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.8-1
- Update to 1.0.8
- Change links to point to github.

* Thu Jan 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.7-1
- Update to 1.0.7
- Apply 9.5 doc layout.

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Fri Sep 25 2015  - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Initial packaging for PostgreSQL RPM Repository
