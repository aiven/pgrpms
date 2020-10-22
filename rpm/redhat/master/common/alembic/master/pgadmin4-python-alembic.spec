%global sname alembic

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.9.7
Release:	4%{?dist}
Summary:	Database migration tool for SQLAlchemy

License:	MIT
URL:		https://pypi.io/project/alembic
Source0:	https://pypi.io/packages/source/a/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
BuildRequires:	python3-dateutil
BuildRequires:	python3-sqlalchemy >= 0.7.4
Requires:       python3-dateutil
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-python3-dateutil
BuildRequires:	pgadmin4-python3-sqlalchemy >= 0.7.4
Requires:       pgadmin4-python3-dateutil
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

%{__install} -d -m 0755 %{buildroot}%{_mandir}/man1

%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}/

# Remove binary, we don't need it in PEM packaging.
%{__rm} %{buildroot}%{_bindir}/%{sname}


%files
%{pgadmin4py3instdir}/%{sname}
%{pgadmin4py3instdir}/%{sname}-*egg-info*

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.7-4
- Switch to PY3 on RHEL 8.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.7-3.1
- Rebuild against PostgreSQL 11.0

* Mon Apr 16 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.7-3
- Initial packaging for PostgreSQL RPM Repo, to satisfy
  pgAdmin4 dependency
