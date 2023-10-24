%global _vpath_builddir .
%global sname	dbt2

Summary:	Database Test 2 Differences from the TPC-C - Common package
Name:		%{sname}-common
Version:	0.53.7
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch0:		%{sname}-cmakelists-rpm.patch
Patch1:		%{sname}-profile.patch

BuildRequires:	gcc-c++ openssl-devel curl-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 3.2.0
%endif

%if 0%{?suse_version} >= 1315
BuildRequires:	libexpat-devel
%else
Requires:	expat-devel
%endif

BuildRequires:	libpq5-devel
Requires:	R

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

This package includes binaries to run the test.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0
%patch -P 1 -p0

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
%doc README
%attr (755,root,root) %{_bindir}/%{sname}*
%{_mandir}/man1/dbt2*

%changelog
* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.7-1PGDG
- Update to 0.53.7
- Add SLES 15 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.6-1PGDG
- Update to 0.53.6

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.4-1PGDG
- Update to 0.53.4
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.50.1-1.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Tue Mar 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.50.1-1
- Update to 0.50.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.49.1-1
- Update to 0.49.1

* Wed Jan 18 2023 Devrim Gündüz <devrim@gunduz.org> - 0.48.7-1
- Update to 0.48.7
- Remove Patch2, already in upstream.

* Sun Aug 28 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Add config file, and docs.

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
