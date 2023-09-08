%global debug_package %{nil}
%global sname pgq

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Generic Queue for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.5.1
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/%{sname}/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel gcc pgdg-srpm-macros

Obsoletes:	%{sname}-%{pgmajorversion} < 3.4.1-2

BuildRequires:	python3-devel

Requires:	python3-psycopg2 postgresql%{pgmajorversion} python3

%description
PgQ is PostgreSQL extension that provides generic, high-performance lockless
queue with simple API based on SQL functions.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgq
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for pgq
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
%{__make}

%install
%{__rm} -rf %{buildroot}

export PG_CONFIG=%{pginstdir}/bin/pg_config
%{__make} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/pgq*.so
%{pginstdir}/share/contrib/*pgq*.sql
%{pginstdir}/share/extension/pgq*.sql
%{pginstdir}/share/extension/pgq*.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}*/*.bc
%endif

%changelog
* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5.1-1PGDG
- Update to 3.5.1
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5-1
- Update to 3.5

* Wed Apr 27 2022 Devrim Gündüz <devrim@gunduz.org> - 3.4.2-1
- Update to 3.4.2
- Split llvmjit into its own subpackage.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1
- Fix LLVM and clang dependencies for aarch64

* Tue Feb 18 2020 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1
- Initial packaging for the PostgreSQL RPM Repo
