%global sname firebird_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	A PostgreSQL foreign data wrapper (FDW) for Firebird
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.1
Release:	1%{dist}
Source:		https://github.com/ibarwick/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/ibarwick/%{sname}
License:	PostgreSQL
Group:		Productivity/Databases/Tools
BuildRequires:	postgresql%{pgmajorversion}-devel firebird-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
# Packages come from EPEL and SCL:
%ifarch aarch64
BuildRequires:	llvm-toolset-7.0-llvm-devel >= 7.0.1 llvm-toolset-7.0-clang >= 7.0.1
%else
BuildRequires:	llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 4.0.1
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
# Packages come from Appstream:
BuildRequires:	llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?fedora}
BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm10-devel clang10-devel
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to Firebird.
It provides both read (SELECT) and write (INSERT/UPDATE/DELETE)
support, WHERE-clause pushdowns, connection caching and Firebird transaction
support.

This code is very much work-in-progress; USE AT YOUR OWN RISK.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
export PG_CONFIG=%{pginstdir}/bin/pg_config
PG_CPPFLAGS="-I%{_includedir}/firebird" USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PG_CONFIG=%{pginstdir}/bin/pg_config
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.1
- Add support for Power.

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Initial packaging for the PostgreSQL RPM repository. This is
  an improved version of the upstream spec file.
