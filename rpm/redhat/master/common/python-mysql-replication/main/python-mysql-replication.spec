%global sname	mysql-replication
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}

Name:		python3-%{sname}
Version:	0.22
Release:	1%{?dist}
Summary:	Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL
License:	Apache-2.0
URL:		https://github.com/noplay/python-mysql-replication
Source0:	https://github.com/noplay/python-mysql-replication/archive/0.22.tar.gz
BuildArch:	noarch

BuildRequires:	python3-setuptools

Requires:	python3-PyMySQL

%description
Pure Python Implementation of MySQL replication protocol build on top of
PyMYSQL. This allow you to receive event like insert, update, delete with
their datas and raw SQL queries.
 Use cases
  -  MySQL to NoSQL database replication
  -  MySQL to search engine replication
  -  Invalidate cache when something change in database
  -  Audit
  -  Real time analytics

%prep
%setup -q -n python-%{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --prefix=%{_prefix} --root=%{buildroot} -O2

%clean
%{__rm} -rf %{buildroot}

%files
%{python3_sitelib}/mysql_replication-%{version}-py%{pyver}.egg-info/*
%{python3_sitelib}/pymysqlreplication/*.py*
%{python3_sitelib}/pymysqlreplication/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/constants/*.py*
%{python3_sitelib}/pymysqlreplication/constants/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/tests/*.py*
%{python3_sitelib}/pymysqlreplication/tests/__pycache__/*.py*

%changelog
* Wed Dec 9 2020 - Devrim Gündüz <devrim@gunduz.org> 0.22-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency.
