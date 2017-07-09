%global         sname sqlparse

%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/


Name:           pgadmin4-python-%{sname}
Version:        0.2.1
Release:        4%{?dist}
Summary:        Non-validating SQL parser for Python

Group:          Development/Languages
License:        BSD
URL:            https://github.com/andialbrecht/%{sname}
Source0:        https://github.com/andialbrecht/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytools
%endif
%else
BuildRequires:	python2-devel python-tools
%endif
BuildRequires:  python-setuptools
BuildRequires:  python-py

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
* Fri Apr 21 2017 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-4
- Remove binary, we don't need it in this package.

* Tue Apr 11 2017 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-3
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
