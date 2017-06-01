%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global sname backports.csv

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	1.0.5
Release:	2%{?dist}
Epoch:		1
Summary:	Backport of Python 3 csv module

License:	BSD
URL:		https://pypi.python.org/pypi/backports.csv
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{sname}}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%else
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
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
%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
%else
CFLAGS="%{optflags}" %{__ospython2} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/backports %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}-nspkg.pth %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%{__mv} build/lib/backports/__init__.py %{buildroot}/%{pgadmin4py3instdir}/backports

%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/backports %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}-nspkg.pth %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%{__mv} build/lib/backports/__init__.py %{buildroot}/%{pgadmin4py2instdir}/backports
%endif # with_python3

%files
%if 0%{?with_python3}
%doc README.rst
%license LICENSE.rst
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/backports
%{pgadmin4py3instdir}%{sname}-%{version}-py%{py3ver}-nspkg.pth
%else
%doc README.rst LICENSE.rst
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/backports
%{pgadmin4py2instdir}%{sname}-%{version}-py%{py2ver}-nspkg.pth
%endif

%changelog
* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-2
- Also install __init__py. manually.

* Thu Jun 1 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.5-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
