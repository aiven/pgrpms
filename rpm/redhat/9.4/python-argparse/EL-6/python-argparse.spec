%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global oname  argparse

Summary:       Optparse inspired command line parser for Python
Name:          python-argparse
Version:       1.2.1
Release:       3%{?dist}
License:       Python
Group:         Development/Languages
URL:           http://code.google.com/p/argparse/
Source0:       http://argparse.googlecode.com/files/argparse-%{version}.tar.gz
BuildRequires: python-setuptools
BuildRequires: dos2unix
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

The argparse module is an optparse-inspired command line parser that
improves on optparse by:
 * handling both optional and positional arguments
 * supporting parsers that dispatch to sub-parsers
 * producing more informative usage messages
 * supporting actions that consume any number of command-line args
 * allowing types and actions to be specified with simple callables 
    instead of hacking class attributes like STORE_ACTIONS or CHECK_METHODS 

as well as including a number of other more minor improvements on the
optparse API.

%prep
%setup -q -n %{oname}-%{version}
dos2unix -k NEWS.txt
%{__rm} -rf doc/source

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check
pushd test
PYTHONPATH=../ %{__python} test_%{oname}.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.txt LICENSE.txt NEWS.txt doc/*
%{python_sitelib}/*

%changelog
* Thu Jul 20 2014 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-3
- Initial version for PostgreSQL RPM repository to satisfy
  barman dependency.
