%global debug_package %{nil}
%global _vpath_builddir .
%global sname	dbt2

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Database Test 2 Differences from the TPC-C - Extensions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.48.3
Release:	3%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch0:		%{sname}-cmakelists-rpm.patch
Requires:	%{sname}-common

BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake => 3.2.0
%endif

BuildRequires:	libpq5-devel openssl-devel curl-devel expat-devel

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for dbt2-extensions
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for dbt2-extensions
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

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
make DESTDIR=%{buildroot}
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
make DESTDIR=%{buildroot} install
popd

# Install extrension control file
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/lib
%{__cp} storedproc/pgsql/c/%{sname}.control %{buildroot}/%{pginstdir}/share/extension
%{__cp} storedproc/pgsql/c/%{sname}.so %{buildroot}/%{pginstdir}/lib
%{__cp} storedproc/pgsql/c/%{sname}--0.45.0.sql %{buildroot}/%{pginstdir}/share/extension/%{sname}--%{version}.sql

# Remove binaries, they are installed with the common package.
%{__rm} -f %{buildroot}/%{_bindir}/*

%clean
%{__rm} -rf %{buildroot}

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
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Aug 17 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Foo

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
