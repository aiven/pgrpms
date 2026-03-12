%global debug_package %{nil}
%global sname	plprofiler

%global plprofilermajver 4
%global plprofilermidver 2
%global plprofilerminver 5

%global git_tag	REL%{plprofilermajver}_%{plprofilermidver}_%{plprofilerminver}
%global ppmajorver %{plprofilermajver}.%{plprofilermidver}

%{!?llvm:%global llvm 1}

Name:		%{sname}-client
Version:	%{ppmajorver}.5
Release:	5PGDG%{dist}
Summary:	Command Line Tool for the PL/pgSQL profiler
License:	Artistic-1.0, CDDL-1.0
URL:		https://github.com/bigsql/%{sname}
Source0:	https://github.com/bigsql/%{sname}/archive/refs/tags/%{git_tag}.tar.gz

AutoReqProv:	no

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

BuildRequires:	python3-six >= 1.4

Requires:	python3
Requires:	python3-psycopg2
Obsoletes:	%{sname}_18-client < 4.2.5-5 %{sname}_17-client < 4.2.5-5
Obsoletes:	%{sname}_16-client < 4.2.5-5 %{sname}_15-client < 4.2.5-5
Obsoletes:	%{sname}_14-client < 4.2.5-5

%description
Command Line Tool for the PL/pgSQL profiler

%prep
%setup -q -n %{sname}-%{git_tag}

%build
cd python-%{sname}
%pyproject_wheel
cd ..

%install
cd python-%{sname}
%pyproject_install
cd ..

%files
%{_bindir}/%{sname}

%dir %{python3_sitelib}/%{sname}_client-%{plprofilermajver}.%{plprofilermidver}.dist-info/
%{python3_sitelib}/%{sname}_client-%{plprofilermajver}.%{plprofilermidver}.dist-info/*
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/*

%changelog
* Wed Feb 4 2026 Devrim Gündüz <devrim@gunduz.org> - 4.2.5-5PGDG
- Initial packaging for the PostgreSQL RPM repository. Fixes
  https://github.com/pgdg-packaging/pgdg-rpms/issues/152
