%global debug_package %{nil}

%global sname pgbson

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	BSON support for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	2%{?dist}.1
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-pgconfig.patch
URL:		http://pgxn.org/dist/pgbson
BuildRequires:	postgresql%{pgmajorversion}-devel, boost-devel
%if 0%{?rhel} && 0%{?rhel} == 6
BuildRequires:	cmake28
%else
BuildRequires:	cmake
%endif
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pgbson is a PostgreSQL extension to manage partitioned tables by time or ID.
This PostgreSQL extension brings BSON data type, together with functions to
create, inspect and manipulate BSON objects.

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
# Create build directory:
%{__rm} -rf ../%{sname}-%{version}-build
%{__mkdir} ../%{sname}-%{version}-build
cd ../%{sname}-%{version}-build
# Start building
%if 0%{?rhel} && 0%{?rhel} == 6
cmake28 ../%{sname}-%{version}
%else
cmake ../%{sname}-%{version}
%endif
%{__make}

%install
%{__rm} -rf %{buildroot}
cd ../%{sname}-%{version}-build
%{__make} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 ../%{sname}-%{version}/README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/pgbson.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/lib/libpgbson.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue Dec 17 2013 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-2
- Unified spec file for all distros.
- Use more macros in spec file
- Update license


* Tue Dec 17 2013 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Thu Oct 31 2013 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
