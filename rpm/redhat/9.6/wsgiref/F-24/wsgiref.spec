%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	WSGI (PEP 333) Reference Library
Name:		wsgiref
Version:	0.1.2
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/wsgiref
Source0:	http://pypi.python.org/packages/source/w/%{name}/%{name}-%{version}.zip
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a standalone release of the wsgiref library, that
provides validation support for WSGI 1.0.1 (PEP 3333) for
Python versions < 3.2, and includes the new
wsgiref.util.test() utility function.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.txt
%dir %{python_sitelib}/wsgiref/
%{python_sitelib}/wsgiref/*
%{python_sitelib}/wsgiref-%{version}-py%{pyver}.egg-info/*

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.1.2-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
