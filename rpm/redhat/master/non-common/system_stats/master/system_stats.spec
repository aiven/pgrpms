%global sname system_stats

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	A Postgres extension for exposing system metrics such as CPU, memory and disk information
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2%{dist}
License:	AGPLv3
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v1.0.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
system_stats is a Postgres extension that provides functions to access system
level statistics that can be used for monitoring. It supports Linux, macOS and
Windows.

Note that not all values are relevant on all operating systems. In such cases
NULL is returned for affected values.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/include/server/extension/%{sname}/%{sname}.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
  %endif
 %endif
%endif

%changelog
* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Remove pgxs patches, and export PATH instead.

* Thu Jun 25 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
