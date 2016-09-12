%global pypi_name pbr

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
Version:        1.8.1
Release:        5%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        http://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires: python-sphinx >= 1.1.3

%description
PBR is a library that injects some useful and sensible default behaviors into
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18
different projects each with at least 3 active branches, it seems like a good
time to make that code into a proper re-usable library.

%package -n python2-%{pypi_name}
Summary:        Python Build Reasonableness
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


%description -n python2-%{pypi_name}
Manage dynamic plugins for Python applications


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Python Build Reasonableness
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel

%description -n python3-%{pypi_name}
Manage dynamic plugins for Python applications
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
export SKIP_PIP_INSTALL=1
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pbr/tests

%if 0%{?do_test}
%check
%{__python} setup.py test
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc html README.rst
%{_bindir}/pbr
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{pypi_name}

%if 0%{?with_python3}
%files -n python3-pbr
%license LICENSE
%doc html README.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog
* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-5
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.

