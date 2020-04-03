%global sname backports.csv

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30  || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-python3-%{sname}
Version:	1.0.5
Release:	4%{?dist}
Epoch:		1
Summary:	Backport of Python 3 csv module

License:	BSD
URL:		https://pypi.python.org/pypi/backports.csv
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%description
The API of the csv module in Python 2 is drastically different from the
csv module in Python 3. This is due, for the most part, to the difference
between str in Python 2 and Python 3.

The semantics of Python 3’s version are more useful because they support
unicode natively, while Python 2’s csv does not.

%prep
%setup -q -n %{sname}-%{version}

%build
CFLAGS="%{optflags}" %{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/backports %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}-nspkg.pth %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%{__mv} build/lib/backports/__init__.py %{buildroot}/%{pgadmin4py3instdir}/backports

%files
%license LICENSE.rst
%doc README.rst
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/backports
%{pgadmin4py3instdir}%{sname}-%{version}-py%{pyver}-nspkg.pth

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-4
- Switch to PY3 on RHEL 7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-3.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-2
- Also install __init__py. manually.

* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
