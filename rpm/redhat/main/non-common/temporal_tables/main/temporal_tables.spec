%global sname temporal_tables

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Temporal tables extension for PostgreQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
Release:	3PGDG%{dist}
Source0:	https://github.com/arkhipov/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/arkhipov/%{sname}
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for temporal_tables
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for temporal_tables
%endif

%description
A temporal table is a table that records the period of time when a row
is valid. There are two types of periods: the application period (also
known as valid-time or business-time) and the system period (also known
as transaction-time).

Currently, Temporal Tables Extension supports the system-period
temporal tables only.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-, root, root)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
	%{pginstdir}/lib/bitcode/%{sname}*.bc
	%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-3PGDG
- Update LLVM dependencies

* Thu Jan 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-2PGDG
- Remove LLVM conditionals. Future updates will all have LLVM enabled
  anyway. This actually fixes RHEL 8 builds, where *for some reason* spectool
  cannot download sources when llvm macro is around just for this spec file.
  This does not fix PostgreSQL bug #18289 in full:
  https://www.postgresql.org/message-id/18289-cc1b88346b51af93%40postgresql.org
  but at least we provide user the RPM.

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository.

