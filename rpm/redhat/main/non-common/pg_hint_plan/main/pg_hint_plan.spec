%global sname	pg_hint_plan

%if %{pgmajorversion} == 16
%global pghintplanversion 1.6.0
%global git_tag	1_6_0
%endif
%if %{pgmajorversion} == 15
%global pghintplanversion 1.5.1
%global git_tag	1_5_0
%endif
%if %{pgmajorversion} == 14
%global pghintplanversion 1.4.2
%global git_tag	1_4_2
%endif
%if %{pgmajorversion} == 13
%global pghintplanversion 1.3.9
%global git_tag	1_3_9
%endif
%if %{pgmajorversion} == 12
%global pghintplanversion 1.3.9
%global git_tag	1_3_9
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Tweak PostgreSQL execution plans using so-called "hints" in SQL comments
Name:		%{sname}_%{pgmajorversion}
Version:	%{pghintplanversion}
Release:	1PGDG%{?dist}
License:	MIT
Source0:	https://github.com/ossc-db/pg_hint_plan/archive/refs/tags/REL%{pgmajorversion}_%{git_tag}.tar.gz
URL:		https://github.com/ossc-db/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
pg_hint_plan makes it possible to tweak PostgreSQL execution plans using so-called
"hints" in SQL comments, like /*+ SeqScan(a) */.

PostgreSQL uses a cost-based optimizer, which utilizes data statistics, not static
rules. The planner (optimizer) esitimates costs of each possible execution plans for a
SQL statement then the execution plan with the lowest cost finally be executed.
The planner does its best to select the best best execution plan, but is not always perfect,
since it doesn't count some properties of the data, for example, correlation between columns.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_hint_plan
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
This packages provides JIT support for pg_hint_plan
%endif

%prep
%setup -q -n %{sname}-REL%{pgmajorversion}_%{git_tag}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%if %{pgmajorversion} >= 14
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md
%endif

%files
%defattr(-,root,root,-)
%if %{pgmajorversion} >= 14
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 12 2023 Devrim Gunduz <devrim@gunduz.org> - %{pghintplanversion}-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
