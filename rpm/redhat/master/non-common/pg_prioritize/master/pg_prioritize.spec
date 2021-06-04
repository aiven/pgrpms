%global sname prioritize
%global pname pg_%{sname}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Get and set the nice priorities of PostgreSQL backends
Name:		%{pname}_%{pgmajorversion}
Version:	1.0.4
Release:	2%{?dist}
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/schmiddy/%{pname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This module implements an interface to getpriority() and setpriority()
for PostgreSQL backends, callable from SQL functions. Essentially,
this module allows users to `renice' their backends.

The priority values are used by getpriority() and setpriority(),
which you may be familiar with from the nice or renice programs.

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
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.*

%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}*.bc
  %endif
 %endif
%endif

%changelog
* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Remove pgxs patches, and export PATH instead.

* Fri Sep 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Initial packaging for PostgreSQL RPM Repository
