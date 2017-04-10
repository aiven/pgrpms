%global pypi_name fixtures

%if 0%{?fedora} > 23
%global with_python3 1
%else
# EL doesn't have Python 3
%global with_python3 0
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2	%{__python}
%global python2_sitelib %{python_sitelib}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global py2ver %(echo `%{__python} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

Name:           python-%{pypi_name}
Version:        3.0.0
Release:        3%{?dist}
Summary:        Fixtures, reusable state for writing clean tests and more

License:        ASL 2.0 or BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:	https://files.pythonhosted.org/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 0.11

# Requirements
BuildRequires:  python-mock
BuildRequires:  python-testtools >= 0.9.22

Requires:       python-testtools >= 0.9.22
Requires:       python-six

%description
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unit test compatible test cases easy and straight forward.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Fixtures, reusable state for writing clean tests and more
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 0.11

# Requirements
BuildRequires:  python3-mock
BuildRequires:  python3-testtools >= 0.9.22

Requires:       python3-testtools >= 0.9.22
Requires:       python3-six

%description -n python3-%{pypi_name}
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unit test compatible test cases easy and straight forward.

%endif

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3

%install
%{__rm} -rf %{buildroot}
%if 0%{?with_python3}
%{__ospython} setup.py install --skip-build --root %{buildroot}
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-3
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.
