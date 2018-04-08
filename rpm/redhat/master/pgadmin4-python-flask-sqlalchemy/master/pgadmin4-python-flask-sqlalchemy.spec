%global mod_name Flask-SQLAlchemy
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-sqlalchemy
%else
Name:		pgadmin4-python-sqlalchemy
%endif
Version:	2.1
Release:	7%{?dist}
Summary:	Adds SQLAlchemy support to Flask application

Group:		Development/Libraries
License:	BSD
URL:		http://github.com/mitsuhiko/flask-sqlalchemy
Source0:	https://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools python3-flask
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-setuptools pgadmin4-python3-flask
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools pgadmin4-python-flask
%endif

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
CFLAGS="%{optflags}" %{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_sqlalchemy %{buildroot}%{python3_sitelib}/Flask_SQLAlchemy-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_sqlalchemy %{buildroot}%{python2_sitelib}/Flask_SQLAlchemy-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc docs/ README CHANGES PKG-INFO LICENSE
%else
%license LICENSE
%doc docs/ README CHANGES PKG-INFO
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Flask_SQLAlchemy*.egg-info
%{pgadmin4py3instdir}/flask_sqlalchemy
%else
%{pgadmin4py2instdir}/Flask_SQLAlchemy*.egg-info
%{pgadmin4py2instdir}/flask_sqlalchemy
%endif

%changelog
* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-7
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Jul 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-6
- Remove python-flask dependency, it breaks builds on RHEL 6

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-5
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-4
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
