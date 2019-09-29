%global sname backports.csv

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
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
Version:	1.0.5
Release:	3%{?dist}.1
Epoch:		1
Summary:	Backport of Python 3 csv module

License:	BSD
URL:		https://pypi.python.org/pypi/backports.csv
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif

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
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/backports %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}-nspkg.pth %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%{__mv} build/lib/backports/__init__.py %{buildroot}/%{pgadmin4py3instdir}/backports
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/backports %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}-nspkg.pth %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%{__mv} build/lib/backports/__init__.py %{buildroot}/%{pgadmin4py2instdir}/backports
%endif # with_python3

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.rst README.rst
%else
%license LICENSE.rst
%doc README.rst
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/backports
%{pgadmin4py3instdir}%{sname}-%{version}-py%{pyver}-nspkg.pth
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/backports
%{pgadmin4py2instdir}%{sname}-%{version}-py%{pyver}-nspkg.pth
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-3.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-2
- Also install __init__py. manually.

* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
