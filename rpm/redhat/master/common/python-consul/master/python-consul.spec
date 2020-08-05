%global sname consul

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		python3-%{sname}
Version:	1.1.0
Release:	1%{?dist}
Summary:	Python client for Consul

License:	MIT
URL:		https://pypi.org/project/python-%{sname}/
Source0:	https://files.pythonhosted.org/packages/7f/06/c12ff73cb1059c453603ba5378521e079c3f0ab0f0660c410627daca64b7/python-%{sname}-%{version}.tar.gz

BuildArch:	noarch

Requires:	less python3
%if 0%{?rhel} == 7
BuildRequires:	python36-six >= 1.4 python36-requests >= 2.0
%else
BuildRequires:	python3-six >= 1.4 python3-requests >= 2.0
%endif
BuildRequires:	python3-devel python3-setuptools

%description
Python client for Consul (http://www.consul.io/)

%prep
%setup -q -n python-%{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/consul/__pycache__/*
%{python3_sitelib}/consul/*.py
 %{python3_sitelib}/python_%{sname}-%{version}-py%{pyver}.egg-info/*

%changelog
* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
patroni dependency.
