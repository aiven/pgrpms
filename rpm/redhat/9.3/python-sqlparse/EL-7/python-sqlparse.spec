%global         shortname sqlparse

Name:           python-%{shortname}
Version:        0.2.1
Release:        2%{?dist}
Summary:        Non-validating SQL parser for Python

Group:          Development/Languages
License:        BSD
URL:            https://github.com/andialbrecht/%{shortname}
Source0:        https://github.com/andialbrecht/%{shortname}/archive/%{version}/%{shortname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-tools
BuildRequires:  python-setuptools
BuildRequires:  python-py

%description
sqlparse is a tool for parsing SQL strings.  It can generate pretty-printed
renderings of SQL in various formats.

It is a python module, together with a command-line tool.

%prep
%setup -q -n %{shortname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc AUTHORS CHANGELOG README.rst LICENSE
%else
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%endif

%{python2_sitelib}/*
%{_bindir}/sqlformat

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.2.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

