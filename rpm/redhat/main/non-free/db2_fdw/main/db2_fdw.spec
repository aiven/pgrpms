%global debug_package %{nil}
%global sname db2_fdw
%global db2_home "/opt/ibm/db2/V11.5/"

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL DB2 Foreign Data Wrapper
Name:		%{sname}_%{pgmajorversion}
Version:	6.0.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/wolfgangbrandl/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	libstdc++(x86-32) pam(x86-32)

Obsoletes:	%{sname}%{pgmajorversion} < 4.0.0-2

%description
db2_fdw is a PostgreSQL extension that provides a Foreign Data Wrapper for
easy and efficient access to DB2 databases, including pushdown of WHERE
conditions and required columns as well as comprehensive EXPLAIN support.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for db2_fdw
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
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for db2_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
export DB2_HOME="%{db2_home}"
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog

* Fri Sep 29 2023 - Devrim Gündüz <devrim@gunduz.org> 6.0.0-1
- Update to 6.0.0
- Add PGDG branding
- Modernise LLVM portion of the spec file
- Cleanup rpmlint warnings

* Thu Sep 8 2022 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.0.0
- Export PATH for pg_config, so get rid of patches.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 24 2020 - Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0

* Mon Aug 17 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-1
- Update to 3.0.3

* Mon Aug 3 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Tue Jul 28 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Sun Mar 22 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0

* Sat Nov 23 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial packaging for PostgreSQL non-free RPM Repository
