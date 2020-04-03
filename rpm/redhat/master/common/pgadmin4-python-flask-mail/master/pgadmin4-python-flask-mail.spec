%global mod_name Flask-Mail
%global sname flask-mail

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{mod_name}
Summary:	A Flask extension for sending email messages
Version:	0.9.1
Release:	5%{?dist}
License:	Python
URL:		https://pypi.python.org/pypi/Flask-Mail
Source0:	https://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%description
One of the most basic functions in a web application is the ability to
send emails to your users.

The Flask-Mail extension provides a simple interface to set up SMTP with
your Flask application and to send messages from your views and scripts.

%prep
%setup -q -n %{mod_name}-%{version}

%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_mail* %{buildroot}%{python3_sitelib}/__pycache__/flask_mail* %{buildroot}%{python3_sitelib}/Flask_Mail-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.rst
%license LICENSE
%{pgadmin4py3instdir}/Flask_Mail*.egg-info
%{pgadmin4py3instdir}/__pycache__/flask_mail*
%{pgadmin4py3instdir}/flask_mail*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-5
- Switch to PY3 on RHEL 7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-4.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-3
- Move the components under pgadmin web directory, per #2332.
- Don't install PY2 version on Fedora systems, because we can
  avoid the need by using Sphinx 3 on them.

* Sat Nov 12 2016 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-2
- Install both PY2 and PY3 versions for Fedora 24+. Needed to
  build pgadmin3 docs

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
