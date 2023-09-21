%global sname pg_uuidv7

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	v7 UUIDs data type in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	1PGDG%{dist}
License:	MPLv2.0
Source0:	https://github.com/fboulnois/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/fboulnois/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server

%description
A tiny Postgres extension to create valid version 7 UUIDs in Postgres.

These are regular Postgres UUIDs, so they can be used as primary keys,
converted to and from strings, included in indexes, etc:

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_uuidv7
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
This packages provides JIT support for pg_uuidv7
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3.0-1PGDG
- Update to 1.3.0

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2.0-1PGDG
- Update to 1.2.0

* Mon Jul 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.1-1PGDG
- Update to 1.1.1

* Sun Jul 23 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Update to 1.1.0

* Tue Jun 27 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.2-1PGDG
- Update to 1.0.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Fri May 19 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Initial RPM packaging for the PostgreSQL RPM Repository,
