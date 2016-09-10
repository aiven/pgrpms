%if 0%{?fedora} > 21
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%global sname Flask-Mail

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	A Flask extension for sending email messages
%if 0%{?with_python3}
Name:		python3-flask-mail
%else
Name:		python-flask-mail
%endif
Version:	0.9.1
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/Flask-Mail
Source0:	http://pypi.python.org/packages/source/F/%{sname}/%{sname}-%{version}.tar.gz
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
One of the most basic functions in a web application is the ability to
send emails to your users.

The Flask-Mail extension provides a simple interface to set up SMTP with
your Flask application and to send messages from your views and scripts.

%prep
%setup -q -n %{sname}-%{version}

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
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{python_sitelib}/Flask_Mail-%{version}-py%{pyver}.egg-info/*
%{python_sitelib}/flask_mail.py*
%if 0%{?with_python3}
%{python_sitelib}/__pycache__/flask_mail*pyc
%endif

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
