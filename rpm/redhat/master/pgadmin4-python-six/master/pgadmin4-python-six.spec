%global sname six

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif

Version:	1.12.0
Release:	3%{?dist}
Summary:	Python 2 and 3 compatibility utilities

License:	MIT
URL:		https://pypi.python.org/pypi/six
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

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
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/__pycache__/%{sname}.cpyt* %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}%{python2_sitelib}/%{sname}.py* %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%defattr(-, root, root, -)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE documentation/index.rst README.rst
%else
%license LICENSE
%doc documentation/index.rst README.rst
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}*.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}.cpython*
%{pgadmin4py3instdir}/%{sname}.cpython*
%else
%{pgadmin4py2instdir}/%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}*.py*
%endif

%changelog
* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-1
- Update to 1.12.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-3.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-3
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

