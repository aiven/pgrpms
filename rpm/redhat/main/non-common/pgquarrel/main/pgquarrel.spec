%global sname pgquarrel
%global sversion 0_7_0

Summary:	Compares PostgreSQL database schemas (DDL)
Name:		%{sname}
Version:	0.7.0
Release:	2%{?dist}.1
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{sversion}.tar.gz
Patch0:		pgquarrel-libminipath.patch
URL:		https://github.com/eulerto/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel cmake pgdg-srpm-macros
Requires:	postgresql-libs

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
%patch -P 0 -p0

%build
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
%license LICENSE
%attr (755,root,root) %{_bindir}/%{sname}
%{_libdir}/libmini.so

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-2.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0
- Fix packaging

* Sat Nov 30 2019 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Initial packaging for PostgreSQL RPM Repository
