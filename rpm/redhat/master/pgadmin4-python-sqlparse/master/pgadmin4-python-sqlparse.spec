%global	sname sqlparse

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
Version:	0.2.1
Release:	5%{?dist}
Summary:	Non-validating SQL parser for Python

Group:		Development/Languages
License:	BSD
URL:		https://github.com/andialbrecht/%{sname}
Source0:	https://github.com/andialbrecht/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools python3-tools
BuildRequires:	python3-py
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-setuptools python34-tools
BuildRequires:	python34-py
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools python-tools
BuildRequires:	python-py
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytools
%endif
%endif

%description
sqlparse is a tool for parsing SQL strings.  It can generate pretty-printed
renderings of SQL in various formats.

It is a python module, together with a command-line tool.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython2} setup.py build

%install
%{__ospython2} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
# Remove binary, we don't need it.
%{__rm} -f %{buildroot}%{_bindir}/sqlformat

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc AUTHORS CHANGELOG README.rst LICENSE
%else
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%endif
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Mon Apr 9 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-5
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Fri Apr 21 2017 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-4
- Remove binary, we don't need it in this package.

* Tue Apr 11 2017 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-3
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
