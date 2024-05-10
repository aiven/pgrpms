%global sname	pgsphere
%global pname	pg_sphere

%{!?llvm:%global llvm 1}

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.1
Release:	1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/postgrespro/pgsphere/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/postgrespro/pgsphere
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8
BuildRequires:	healpix-c++-devel
%endif
%if 0%{?suse_version} >= 1315
BuildRequires:	healpix_cxx-devel
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pgSphere is a server side module for PostgreSQL. It contains methods for
working with spherical coordinates and objects. It also supports indexing of
spherical objects.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsphere
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pgsphere
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README.%{pname}
%license %{pginstdir}/doc/extension/COPYRIGHT.pg_sphere
%{pginstdir}/lib/pg_sphere.so
%{pginstdir}/share/extension/pg_sphere*.sql
%{pginstdir}/share/extension/pg_sphere.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{pname}.index.bc
    %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
    %{pginstdir}/lib/bitcode/%{pname}/healpix_bare/*bc
%endif

%changelog
* Fri May 10 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 per chages described at:
  https://github.com/postgrespro/pgsphere/releases/tag/1.5.1

* Fri Feb 23 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.4.2-2PGDG
- Add SLES 15 support

* Thu Dec 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
