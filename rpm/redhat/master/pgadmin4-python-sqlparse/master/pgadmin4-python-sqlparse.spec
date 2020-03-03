%global	sname sqlparse

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 27 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.2.4
Release:	2%{?dist}
Summary:	Non-validating SQL parser for Python

License:	BSD
URL:		https://github.com/andialbrecht/%{sname}
Source0:	https://github.com/andialbrecht/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools python3-tools

%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
BuildRequires:	python3-py
%endif

%description
sqlparse is a tool for parsing SQL strings.  It can generate pretty-printed
renderings of SQL in various formats.

It is a python module, together with a command-line tool.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

# Remove binary, we don't need it.
%{__rm} -f %{buildroot}%{_bindir}/sqlformat

%files
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.2.4-2
- Switch to Python3 on RHEL 7.


* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2.4-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2.4-1
- Update to 0.2.4

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
