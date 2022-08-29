%global _vpath_builddir .
%global sname	dbt2

Summary:	Database Test 2 Differences from the TPC-C - Common package
Name:		%{sname}-common
Version:	0.48.3
Release:	2%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch0:		%{sname}-cmakelists-rpm.patch
Patch1:		%{sname}-profile.patch
Patch2:		%{sname}-pgsql-db-stat-mkdir.patch

BuildRequires:	gcc-c++ openssl-devel curl-devel expat-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 3.2.0
%endif

BuildRequires:	libpq5-devel

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

This package includes binaries to run the test.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build

CFLAGS="$CFLAGS -I%{pginstdir}/include/server -g -fPIE"; export CFLAGS

%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake ..
%else
%cmake3 ..
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

# Remove .sql files, we'll ship them with -extensions  subpackages.
%{__rm} -f %{buildroot}/%{_datadir}/pgsql/*.sql

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/
%{__cp} examples/dbt2_profile %{buildroot}/%{_sysconfdir}/dbt2_profile.conf

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%config %{_sysconfdir}/dbt2_profile.conf
%doc README doc/dbt2-architecture.txt  doc/dbt2-tpc.txt  doc/dbt2-user-guide.txt
%attr (755,root,root) %{_bindir}/%{sname}-*

%changelog
* Sun Aug 28 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Add config file, and docs.

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
