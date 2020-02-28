%global sname click

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25 || 0%{?rhel} == 7
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	6.7
Release:	8%{?dist}.1
Summary:	Simple wrapper around optparse for powerful command line utilities

License:	BSD
URL:		https://github.com/mitsuhiko/click
Source0:	%{url}/archive/%{version}/%{sname}-%{version}.tar.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=1500962
# https://github.com/pallets/click/pull/838
Patch0:		0001-Remove-outdated-comment-about-Click-3.0.patch
Patch1:		0002-Add-pytest-option-to-not-capture-warnings.patch
Patch2:		0003-Catch-and-test-pytest-warning.patch

BuildArch:	noarch

%if 0%{?fedora} > 25 || 0%{?rhel} == 7
BuildRequires:	python3-devel python3-setuptools
%endif

%description
click is a Python package for creating beautiful command line\
interfaces in a composable way with as little amount of code as necessary.\
It's the "Command Line Interface Creation Kit".  It's highly configurable but\
comes with good defaults out of the box.

%prep
%autosetup -n %{sname}-%{version} -p1

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README
%else
%license LICENSE
%doc README
%endif
%if 0%{?with_python3}
%{python3_sitelib}/%{sname}-*.egg-info/
%{python3_sitelib}/%{sname}/
%else
%{python2_sitelib}/%{sname}-*.egg-info/
%{python2_sitelib}/%{sname}/
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 6.7-8.1
- Rebuild against PostgreSQL 11.0

* Mon Apr 9 2018 Devrim Gündüz <devrim@gunduz.org> - 6.7-8
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pgadmin4 dependency on RHEL 6.
