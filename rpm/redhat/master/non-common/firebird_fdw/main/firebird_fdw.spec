%global sname firebird_fdw

Summary:	A PostgreSQL foreign data wrapper (FDW) for Firebird
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	1%{dist}
Source:		https://github.com/ibarwick/%{sname}/archive/1.2.0.tar.gz
URL:		https://github.com/ibarwick/%{sname}
License:	PostgreSQL
Group:		Productivity/Databases/Tools
BuildRequires:	postgresql%{pgmajorversion}-devel firebird-devel
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

%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to Firebird.
It provides both read (SELECT) and write (INSERT/UPDATE/DELETE)
support, WHERE-clause pushdowns, connection caching and Firebird transaction
support.

This code is very much work-in-progress; USE AT YOUR OWN RISK.

%prep
%setup -q -n %{sname}-%{version}

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
PG_CPPFLAGS="-I/usr/include/firebird" USE_PGXS=1 %{__make} %{?_smp_mflags}

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

%if 0%{?rhel} && 0%{?rhel} >= 7
%exclude %{pginstdir}/lib/bitcode
%endif

%changelog
* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Initial packaging for the PostgreSQL RPM repository. This is
  an improved version of the upstream spec file.
