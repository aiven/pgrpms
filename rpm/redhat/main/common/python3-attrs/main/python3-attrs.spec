%global pypi_name attrs
%global sname attr

%global __ospython %{_bindir}/python3.9
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:           python3-attrs
Version:        22.1.0
Release:        1%{?dist}
Summary:        Python attributes without boilerplate

License:        MIT
URL:            http://www.attrs.org/
BuildArch:      noarch
Source0:        https://github.com/hynek/%{pypi_name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  python39-devel
BuildRequires:  python39-setuptools

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/py.typed
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}/*.py*
%{python3_sitelib}/%{pypi_name}/py.typed
%{python3_sitelib}/%{pypi_name}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}-%{version}-py%{pyver}.egg-info

%changelog
* Sun Sep 18 2022 Devrim Gunduz <devrim@gunduz.org>  - 22.1.0-1
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.
