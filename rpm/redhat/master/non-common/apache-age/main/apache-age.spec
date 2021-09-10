%global sname apache-age

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Summary:	A Graph Extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.5.0
Release:	1%{dist}
License:	AGPLv3
URL:		https://github.com/apache/incubator-age
Source0:	https://github.com/apache/incubator-age/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel flex
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Apache AGE is a PostgreSQL Extension that provides graph database
functionality. AGE is an acronym for A Graph Extension, and is
inspired by Bitnine's fork of PostgreSQL 10, AgensGraph, which
is a multi-model database. The goal of the project is to create
single storage that can handle both relational and graph model
data so that users can use standard ANSI SQL along with openCypher,
the Graph query language.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for Citus
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} == 1315
Requires:	llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:	llvm10
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for Age
%endif

%prep
%setup -q -n incubator-age-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{pginstdir}/lib/age.so
%{pginstdir}/share/extension/age--%{version}.sql
%{pginstdir}/share/extension/age.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/age*.bc
    %{pginstdir}/lib/bitcode/age/src/backend/*.bc
    %{pginstdir}/lib/bitcode/age/src/backend/*.bc
    %{pginstdir}/lib/bitcode/age/src/backend/*/*.bc
    %{pginstdir}/lib/bitcode/age/src/backend/*/*/*.bc
%endif

%changelog
* Thu Apr 8 2021 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Sat Mar 6 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Initial packaging for PostgreSQL RPM repository.
