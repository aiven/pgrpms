%global sname pgquarrel
%global sversion 0_6_0
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Compares PostgreSQL database schemas (DDL)
Name:		%{sname}%{sversion}
Version:	0.6.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{sversion}.tar.gz
URL:		https://github.com/eulerto/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel cmake
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pgquarrel is a program that compares PostgreSQL database schemas (DDL).

Given two database connections, it output a file that represent the
difference between schemas. It means that if you run the output file into
the target database, it'll have the same schema as the source database.
The main use case is to deploy database changes into testing, staging or
production environment.

pgquarrel does not rely on another tool (such as pg_dump) instead it connects
directly to PostgreSQL server, obtain meta data from catalog, compare objects
and output the commands necessary to turn target database into source
database.

%prep
%setup -q -n %{sname}-%{sname}_%{sversion}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

cmake -DPGCONFIG_PATH=/usr/pgsql-%{pgmajorversion}/bin/pg_config \
	-DCMAKE_INSTALL_PREFIX=%{pginstdir} .

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/%{sname}
%{pginstdir}/lib/libmini.so

%changelog
* Sat Nov 30 2019 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Initial packaging for PostgreSQL RPM Repository
