%global debug_package %{nil}
%global sname	rollbar
%global realver	1.4.0
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}

Name:		python3-%{sname}
Summary:	Python notifier for reporting exceptions, errors, and log messages to Rollbar.
Version:	0.15.1
Release:	1%{?dist}
URL:		https://github.com/%{sname}/py%{sname}
Source0:	https://github.com/%{sname}/py%{sname}/archive/v%{version}.tar.gz
License:	Python-2.0

BuildRequires:	python3-setuptools

Requires:	python3-requests

%description
The rollbar module makes it easy to write user friendly command line interfaces.

The program defines what arguments it requires, and rollbar will figure out how
to parse those out of sys.argv. The rollbar module also automatically generates
help and usage messages and issues errors when users give the program invalid
arguments.

As of Python >= 2.7 and >= 3.2, the rollbar module is maintained within the
Python standard library. For users who still need to support Python < 2.7
or < 3.2, it is also provided as a separate package, which tries to stay
compatible with the module in the standard library, but also supports older
Python versions.

%prep
%setup -q -n pyrollbar-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --prefix=%{_prefix} --root=%{buildroot} -O2

%clean
%{__rm} -rf %{buildroot}

%files
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info/*
%{python3_sitelib}/%{sname}/__pycache__/*.py*
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/contrib/*.py*
%{python3_sitelib}/%{sname}/contrib/__pycache__/*py*
%{python3_sitelib}/%{sname}/contrib/bottle/*.py*
%{python3_sitelib}/%{sname}/contrib/bottle/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/django/*.py*
%{python3_sitelib}/%{sname}/contrib/django/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/django_rest_framework/*.py*
%{python3_sitelib}/%{sname}/contrib/django_rest_framework/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/flask/*.py*
%{python3_sitelib}/%{sname}/contrib/flask/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/pyramid/*.py*
%{python3_sitelib}/%{sname}/contrib/pyramid/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/quart/*.py*
%{python3_sitelib}/%{sname}/contrib/quart/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/rq/*.py*
%{python3_sitelib}/%{sname}/contrib/rq/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/*.py*
%{python3_sitelib}/%{sname}/lib/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/filters/*.py*
%{python3_sitelib}/%{sname}/lib/filters/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/transforms/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/transforms/*.py*
%{python3_sitelib}/%{sname}/test/*.py*
%{python3_sitelib}/%{sname}/test/__pycache__/*.py*
%{python3_sitelib}/%{sname}/test/flask_tests/*.py*
%{python3_sitelib}/%{sname}/test/flask_tests/__pycache__/*.py*
%{python3_sitelib}/%{sname}/test/twisted_tests/*.py*
%{python3_sitelib}/%{sname}/test/twisted_tests/__pycache__/*.py*

%changelog
* Wed Dec 9 2020 - Devrim Gündüz <devrim@gunduz.org> 0.15.1-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency.
