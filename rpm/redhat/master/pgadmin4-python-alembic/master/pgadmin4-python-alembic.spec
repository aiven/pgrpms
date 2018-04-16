%global sname alembic

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
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif

Version:	0.9.7
Release:	3%{?dist}
Summary:	Database migration tool for SQLAlchemy

Group:		Development/Libraries
License:	MIT
URL:		https://pypi.io/project/alembic
Source0:	https://pypi.io/packages/source/a/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
BuildRequires:	python3-mock python3-dateutil
BuildRequires:	python3-editor python3-pytest
BuildRequires:	python3-sqlalchemy >= 0.7.4
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname}
BuildRequires:	python34-devel python34-setuptools
BuildRequires:	python34-mock pgadmin4-python3-dateutil
BuildRequires:	python34-pytest
BuildRequires:	python34-sqlalchemy >= 0.7.4
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
BuildRequires:	python-mock python-dateutil
BuildRequires:	pytest
BuildRequires:	python-sqlalchemy >= 0.7.4
%endif


%global _description\
Alembic is a new database migrations tool, written by the author of\
SQLAlchemy.  A migrations tool offers the following functionality:\
\
* Can emit ALTER statements to a database in order to change the structure\
  of tables and other constructs.\
* Provides a system whereby "migration scripts" may be constructed; each script\
  indicates a particular series of steps that can "upgrade" a target database\
  to a new version, and optionally a series of steps that can "downgrade"\
  similarly, doing the same steps in reverse.\
* Allows the scripts to execute in some sequential manner.\
\
Documentation and status of Alembic is at http://readthedocs.org/docs/alembic/

%description %_description

%prep
%setup -q -n %{sname}-%{version}

# Make sure that epel/rhel picks up the correct version of sqlalchemy
%if 0%{?rhel} && 0%{?rhel} <= 6
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"sqlalchemy>=0.6\", \"nose>=0.11\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py
%endif

%build
%{__ospython} setup.py build

%install

install -d -m 0755 %{buildroot}%{_mandir}/man1

%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}/
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}/
%endif

# Remove binary, we don't need it in PEM packaging.
%{__rm} %{buildroot}%{_bindir}/%{sname}


%files
%if 0%{?with_python3}
%{pgadmin4py3instdir}/%{sname}
%{pgadmin4py3instdir}/%{sname}-*egg-info*
%else
%{pgadmin4py2instdir}/%{sname}
%{pgadmin4py2instdir}/%{sname}-*egg-info*
%endif

%changelog
* Mon Apr 16 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.7-3
- Initial packaging for PostgreSQL RPM Repo, to satisfy
  pgAdmin4 dependency
