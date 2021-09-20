%global sname credcheck

%pgdg_set_llvm_variables

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1%{?dist}
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/MigOpsRepos/%{sname}
Source0:	https://github.com/MigOpsRepos//%{sname}/archive/refs/tags/v0.2.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.15
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
The credcheck PostgreSQL extension provides few general credential checks,
which will be evaluated during the user creation, during the password change
and user renaming. By using this extension, we can define a set of rules to
allow a specific set of credentials, and a set of rules to reject a certain
type of credentials. This extension is developed based on the PostgreSQL's
check_password_hook hook.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif
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
%if 0%{?isllvm}
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
 %endif
%else
%endif

%changelog
* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Initial packaging for PostgreSQL YUM repository.

* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.1-2
- Initial packaging for PostgreSQL YUM repository.

