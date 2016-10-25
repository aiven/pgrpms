%if 0%{?fedora} > 21
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	HTML minifier for Python
Name:		django-htmlmin
Version:	0.9.1
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/django-htmlmin
Source0:	http://pypi.python.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
django-html is an HTML minifier for Python, with full support for HTML
5. It supports Django, Flask and many other Python web frameworks. It
also provides a command line tool, that can be used for static websites
or deployment scripts.

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.rst
%{_bindir}/pyminify
%dir %{python_sitelib}/htmlmin/
%dir %{python_sitelib}/django_htmlmin-%{version}-py%{pyver}.egg-info/
%{python_sitelib}/htmlmin/*
%{python_sitelib}/django_htmlmin-%{version}-py%{pyver}.egg-info/*

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> -0.9.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
