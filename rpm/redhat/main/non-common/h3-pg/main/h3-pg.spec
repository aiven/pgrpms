%global _vpath_builddir .
%global sname	h3-pg

Summary:	Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.1.3
Release:	2PGDG%{dist}
License:	Apache
URL:		https://github.com/zachasme/%{sname}
Source0:	https://github.com/zachasme/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-useosh3.patch
BuildRequires:	cmake >= 3.20 h3-devel
BuildRequires:	postgresql%{pgmajorversion}-devel

Requires:	postgresql%{pgmajorversion} h3

%description
This library provides PostgreSQL bindings for the H3 Core Library.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_BUILD_TYPE=Release .. \
%else
%cmake3 .. -DCMAKE_BUILD_TYPE=Release .. \
%endif
	-DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config
popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%{pginstdir}/lib/h3.so
%{pginstdir}/lib/h3_postgis.so
%{pginstdir}/share/extension/h3*.sql
%{pginstdir}/share/extension/h3.control
%{pginstdir}/share/extension/h3_postgis.control

%changelog
* Thu May 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-2PGDG
- Fix changelog date.

* Sun Nov 5 2023 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-1PGDG
- Initial packaging of h3-pg.
