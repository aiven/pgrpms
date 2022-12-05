%global sname credcheck

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	2%{?dist}
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/MigOpsRepos/%{sname}
Source0:	https://github.com/MigOpsRepos//%{sname}/archive/refs/tags/v0.2.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.15
Requires:	postgresql%{pgmajorversion}-server

%description
The credcheck PostgreSQL extension provides few general credential checks,
which will be evaluated during the user creation, during the password change
and user renaming. By using this extension, we can define a set of rules to
allow a specific set of credentials, and a set of rules to reject a certain
type of credentials. This extension is developed based on the PostgreSQL's
check_password_hook hook.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for credcheck
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for credcheck
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension//%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-1
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-1
- Initial packaging for PostgreSQL YUM repository.

* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-2
- Initial packaging for PostgreSQL YUM repository.

