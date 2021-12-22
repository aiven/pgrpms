%global debug_package %{nil}
%global sname pgq

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Generic Queue for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.4.1
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/pgq/pgq/archive/v%{version}.tar.gz
URL:		https://github.com/pgq/pgq/
BuildRequires:	postgresql%{pgmajorversion}-devel gcc pgdg-srpm-macros

Obsoletes:	%{sname}-%{pgmajorversion} < 3.4.1-2

%ifnarch ppc64 ppc64le s390 s390x armv7hl
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
%endif

BuildRequires:	python3-devel

Requires:	python3-psycopg2 postgresql%{pgmajorversion} python3

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PgQ is PostgreSQL extension that provides generic, high-performance lockless
queue with simple API based on SQL functions.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

export PG_CONFIG=%{pginstdir}/bin/pg_config
%{__make}

%install
%{__rm} -rf %{buildroot}

export PG_CONFIG=%{pginstdir}/bin/pg_config
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/pgq*.so
%{pginstdir}/share/contrib/*pgq.sql
%{pginstdir}/share/contrib/pgq*.sql
%{pginstdir}/share/extension/pgq*.sql
%{pginstdir}/share/extension/pgq*.control

%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}*/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1
- Fix LLVM and clang dependencies for aarch64

* Tue Feb 18 2020 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1
- Initial packaging for the PostgreSQL RPM Repo
