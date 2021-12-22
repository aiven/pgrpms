%global sname pgquarrel
%global sversion 0_7_0

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Compares PostgreSQL database schemas (DDL)
Name:		%{sname}
Version:	0.7.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{sversion}.tar.gz
Patch0:		pgquarrel-libminipath.patch
URL:		https://github.com/eulerto/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel cmake pgdg-srpm-macros
Requires:	postgresql-libs

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
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
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

cmake -DPGCONFIG_PATH=/usr/pgsql-%{pgmajorversion}/bin/pg_config \
	-DCMAKE_INSTALL_PREFIX=/usr .

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
%attr (755,root,root) %{_bindir}/%{sname}
%{_libdir}/libmini.so

%changelog
* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0
- Fix packaging

* Sat Nov 30 2019 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Initial packaging for PostgreSQL RPM Repository
