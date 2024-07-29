%global debug_package %{nil}
%global _vpath_builddir .
%global sname	dbt2

%{!?llvm:%global llvm 1}

Summary:	Database Test 2 Differences from the TPC-C - Extensions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.61.2
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch0:		%{sname}-cmakelists-rpm.patch
Requires:	%{sname}-common

BuildRequires:	gcc-c++
BuildRequires:	cmake => 3.2.0

BuildRequires:	libpq5-devel openssl-devel curl-devel

%if 0%{?suse_version} >= 1315
BuildRequires:	libexpat-devel
%else
Requires:	expat-devel
%endif

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for dbt2-extensions
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for dbt2-extensions
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build

CFLAGS="$CFLAGS -I%{pginstdir}/include/server -g -fPIE"; export CFLAGS
export PATH=%{pginstdir}/bin/:$PATH
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake ..
%else
%cmake3 ..
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

pushd storedproc/pgsql/c
export PATH=%{pginstdir}/bin:$PATH
%{__make} DESTDIR=%{buildroot}
popd

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin/:$PATH
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

pushd storedproc/pgsql/c
export PATH=%{pginstdir}/bin:$PATH
%{__make} DESTDIR=%{buildroot} install
popd

# Install extrension control file
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/lib
%{__cp} storedproc/pgsql/c/%{sname}.control %{buildroot}/%{pginstdir}/share/extension
%{__cp} storedproc/pgsql/c/%{sname}.so %{buildroot}/%{pginstdir}/lib
%{__cp} storedproc/pgsql/c/%{sname}--0.45.0.sql %{buildroot}/%{pginstdir}/share/extension/%{sname}--%{version}.sql

# Remove binaries, they are installed with the common package.
%{__rm} -f %{buildroot}/%{_bindir}/*

# Remove man files, they are installed with the common package.
%{__rm} -f %{buildroot}/%{_mandir}/man1/dbt2*

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/stock_level.sql
%{pginstdir}/share/delivery.sql
%{pginstdir}/share/new_order.sql
%{pginstdir}/share/order_status.sql
%{pginstdir}/share/payment.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 0.61.2-1PGDG
- Update 0.61.2
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 0.53.9-1PGDG
- Update to 0.53.9

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.7-1PGDG
- Update to 0.53.7
- Add SLES 15 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.6-1PGDG
- Update to 0.53.6

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.4-1PGDG
- Update to 0.53.4
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.50.1-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Tue Mar 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.50.1-1
- Update to 0.50.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.49.1-1
- Update to 0.49.1

* Wed Jan 18 2023 Devrim Gündüz <devrim@gunduz.org> - 0.48.7-1
- Update to 0.48.7

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Aug 17 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Foo

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
