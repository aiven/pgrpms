%global sname fixtures
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
Version:	3.0.0
Release:	5%{?dist}.1
Summary:	Fixtures, reusable state for writing clean tests and more

License:	ASL 2.0 or BSD
URL:		https://pypi.python.org/pypi/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/f/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%description
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unit test compatible test cases easy and straight forward.

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-mock
BuildRequires:	pgadmin4-python3-pbr >= 0.11
BuildRequires:	python3-testtools >= 0.9.22
Requires:	python3-testtools >= 0.9.22 python3-six
%endif

%if 0%{?rhel} == 7
BuildRequires:  python2-devel python-mock
BuildRequires:	pgadmin4-python-pbr >= 0.11
BuildRequires:	python-testtools >= 0.9.22
Requires:	python-testtools >= 0.9.22 python-six
%endif

%prep
%autosetup -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-5.1
- Rebuild against PostgreSQL 11.0

* Sat Apr 7 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-5
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-4
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-3
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.
