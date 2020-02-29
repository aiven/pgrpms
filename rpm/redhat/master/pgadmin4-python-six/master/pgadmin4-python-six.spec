%global sname six

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-python3-%{sname}
Version:	1.12.0
Release:	4%{?dist}
Summary:	Python 2 and 3 compatibility utilities

License:	MIT
URL:		https://pypi.python.org/pypi/six
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%description
%%{name} provides simple utilities for wrapping over differences between\
Python 2 and Python 3.

%prep
%autosetup -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/__pycache__/%{sname}.cpyt* %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}/%{pgadmin4py3instdir}

%files
%defattr(-, root, root, -)
%license LICENSE
%doc documentation/index.rst README.rst
%{pgadmin4py3instdir}/%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}*.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}.cpython*
%{pgadmin4py3instdir}/%{sname}.cpython*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-4
- Switch to PY3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-1
- Update to 1.12.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-3.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-3
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

