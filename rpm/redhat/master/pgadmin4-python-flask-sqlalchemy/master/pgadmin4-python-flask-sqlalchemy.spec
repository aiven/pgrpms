%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global mod_name Flask-SQLAlchemy
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

Name:           pgadmin4-python-flask-sqlalchemy
Version:        2.1
Release:        6%{?dist}
Summary:        Adds SQLAlchemy support to Flask application

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mitsuhiko/flask-sqlalchemy
Source0:        https://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask
#Requires:       python-sqlalchemy

%description
Flask-SQLAlchemy is an extension for Flask that adds support for
SQLAlchemy to your application. It aims to simplify using SQLAlchemy with
Flask by providing useful defaults and extra helpers that make it easier
to accomplish common tasks.

%prep
%setup -q -n %{mod_name}-%{version}
%{__rm} -f docs/_static/.DS_Store
%{__rm} -f docs/.DS_Store
%{__rm} -f docs/_themes/.gitignore
chmod -x docs/_static/flask-sqlalchemy-small.png

%build
CFLAGS="%{optflags}" %{__ospython2} setup.py build

%install
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_sqlalchemy %{buildroot}%{python2_sitelib}/Flask_SQLAlchemy-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%doc docs/ README CHANGES PKG-INFO LICENSE
%{pgadmin4py2instdir}/Flask_SQLAlchemy*.egg-info
%{pgadmin4py2instdir}/flask_sqlalchemy

%changelog
* Thu Jul 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-6
- Remove python-flask dependency, it breaks builds on RHEL 6

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-5
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-4
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
