%global pypi_name pbr

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2	%{__python}
%global python2_sitelib %{python_sitelib}
%endif

Name:           python-%{pypi_name}
Version:        1.8.1
Release:        5%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        http://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
PBR is a library that injects some useful and sensible default behaviors into
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18
different projects each with at least 3 active branches, it seems like a good
time to make that code into a proper re-usable library.
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel

%if 0%{?do_test} == 1
BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%build
export SKIP_PIP_INSTALL=1
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pbr/tests

%files
%doc README.rst LICENSE
%{_bindir}/pbr
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{pypi_name}

%changelog
* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-5
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.

