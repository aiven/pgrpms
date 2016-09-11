%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%global sname Flask-Security

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%if 0%{?with_python3}
Name:		python3-flask-security
%else
Name:		python-flask-security
%endif
Summary:	Simple security for Flask apps
Version:	1.7.5
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/%{sname}
Source0:	https://pypi.python.org/packages/source/F/%{sname}/%{sname}-%{version}.tar.gz
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Flask-Security quickly adds security features to your Flask application.

%prep
%setup -q -n %{sname}-%{version}
# Remove irrelevant files:
find . -name "*DS_Store*" -exec rm -rf {} \;

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
%dir %{python_sitelib}/flask_security/
%{python_sitelib}/flask_security/*
%{python_sitelib}/Flask_Security-%{version}-py%{pyver}.egg-info/*

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.5-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
