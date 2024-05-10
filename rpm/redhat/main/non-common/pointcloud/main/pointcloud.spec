%global sname pointcloud
%global pointcloudmajorversion 1.2

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension for storing point cloud (LIDAR) data
Name:		%{sname}_%{pgmajorversion}
Version:	%{pointcloudmajorversion}.5
Release:	1PGDG%{?dist}
URL:		https://github.com/pgpointcloud/%{sname}
Source0:	https://github.com/pgpointcloud/%{sname}/archive/v%{version}.tar.gz
License:	BSD
%if 0%{?suse_version} >= 1315
Requires:	cunit-devel
%else
Requires:	CUnit-devel
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel autoconf libxml2-devel
Requires:	postgresql%{pgmajorversion}-server postgis3_%{pgmajorversion}

%description
LIDAR point cloud are becoming more and more available. Devices are easy to
get, not too expensive, and provide very accurate 3D points. pgPointCLoud is
an open source PostgreSQL extension for storing point cloud data and use it
with PostGIS. It is very easy to use, robust and efficient.

By storing LIDAR points in a PostgreSQL database, pgPointcloud eases many
problems and allows a good integration with other geo-spatial data (vector,
raster) into one common framework : PostGIS.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgpointcloud
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif

%description llvmjit
This packages provides JIT support for pgpointcloud
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
autoupdate
autoconf
%configure --with-pgconfig=%{pginstdir}/bin/pg_config

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/%{sname}-%{pointcloudmajorversion}*.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_postgis-*.sql
%{pginstdir}/share/extension/%{sname}_postgis.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}-%{pointcloudmajorversion}/*.bc
%endif

%changelog
* Fri May 10 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository:
  https://github.com/pgpointcloud/pointcloud/blob/v1.2.5/NEWS

