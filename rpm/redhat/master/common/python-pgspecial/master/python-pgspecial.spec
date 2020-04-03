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

%global sname pgspecial
%global srcname pgspecial

%if 0%{?with_python3}
Name:		python3-%{sname}
%else
Name:		python-%{sname}
%endif
Version:	1.8.0
Release:	1%{?dist}.1
Epoch:		1
Summary:	Meta-commands handler for Postgres Database.

License:	BSD
URL:		https://pypi.python.org/pypi/pgspecial
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:	noarch

%description
This package provides an API to execute meta-commands (AKA “special”,
or “backslash commands”) on PostgreSQL.

%prep
%setup -q -n %{srcname}-%{version}

%build
%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
%else
CFLAGS="%{optflags}" %{__ospython2} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
%endif # with_python3


%files
%doc README.rst
%if 0%{?with_python3}
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*
%else
%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info
%dir %{python2_sitelib}/%{sname}
%{python2_sitelib}/%{sname}/*
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgcli dependency.
