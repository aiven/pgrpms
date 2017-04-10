%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global mod_name Flask-SQLAlchemy

Name:           python-flask-sqlalchemy
Version:        2.1
Release:        3%{?dist}
Summary:        Adds SQLAlchemy support to Flask application

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mitsuhiko/flask-sqlalchemy
Source0:        http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask
Requires:       python-sqlalchemy

%description
Flask-SQLAlchemy is an extension for Flask that adds support for
SQLAlchemy to your application. It aims to simplify using SQLAlchemy with
Flask by providing useful defaults and extra helpers that make it easier
to accomplish common tasks.

%if 0%{?with_python3}
%package -n python3-flask-sqlalchemy
Summary:        Adds SQLAlchemy support to Flask application
%{?python_provide:%python_provide python3-%{mod_name}}
%{?python_provide:%python_provide python3-flask-sqlalchemy}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
BuildRequires:  python3-sqlalchemy
Requires:       python3-flask
Requires:       python3-sqlalchemy

%description -n python3-flask-sqlalchemy
Flask-SQLAlchemy is an extension for Flask that adds support for
SQLAlchemy to your application. It aims to simplify using SQLAlchemy with
Flask by providing useful defaults and extra helpers that make it easier
to accomplish common tasks.

Python 3 version.
%endif # with_python3

%prep
%setup -q -n %{mod_name}-%{version}
%{__rm} -f docs/_static/.DS_Store
%{__rm} -f docs/.DS_Store
%{__rm} -f docs/_themes/.gitignore
chmod -x docs/_static/flask-sqlalchemy-small.png

%build
CFLAGS="%{optflags}" %{__ospython2} setup.py build

%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
%endif # with_python3

%{__ospython2} setup.py install --skip-build --root %{buildroot}


%files
%doc docs/ README CHANGES PKG-INFO LICENSE
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/flask_sqlalchemy/

%if 0%{?with_python3}
%files -n python3-flask-sqlalchemy
%doc docs/ README CHANGES PKG-INFO LICENSE
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_sqlalchemy/
%endif # with_python3

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-4
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
