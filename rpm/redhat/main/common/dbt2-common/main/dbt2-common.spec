%global _vpath_builddir .
%global sname	dbt2

Summary:	Database Test 2 Differences from the TPC-C - Common package
Name:		%{sname}-common
Version:	0.48.3
Release:	1%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch0:		%{sname}-cmakelists-rpm.patch

BuildRequires:	gcc-c++
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

%clean
%{__rm} -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README
%{_bindir}/%{sname}-*

%changelog
* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
