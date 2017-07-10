%global pypi_name Flask-Migrate
%global sname	flask-migrate

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

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/


%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	2.0.4
Release:	1%{?dist}
Summary:	SQLAlchemy database migrations for Flask applications using Alembic

License:	MIT
URL:		https://github.com/miguelgrinberg/%{pypi_name}
Source0:	https://github.com/miguelgrinberg/%{pypi_name}/archive/v%{version}.tar.gz
BuildArch:	noarch

%if %{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%else
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%else
BuildRequires:	python2-devel
%endif
BuildRequires:	python-setuptools
%endif

%if %{?with_python3}
Requires:	pgadmin4-python3-flask
%else
Requires:	pgadmin4-python-flask
%endif

%description
lask-Migrate is an extension that handles SQLAlchemy database migrations
for Flask applications using Alembic. The database operations are
provided as command line arguments for Flask-Script.

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info


%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py build
popd
%else
%{__ospython2} setup.py build
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_migrate %{buildroot}%{python3_sitelib}/Flask_Migrate-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_migrate %{buildroot}%{python2_sitelib}/Flask_Migrate-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%endif

%files
%if 0%{?with_python3}
%doc README.md
%license LICENSE
%{pgadmin4py3instdir}/Flask_Migrate*.egg-info
%{pgadmin4py3instdir}/flask_migrate/*

%else
%doc README.md LICENSE
%{pgadmin4py2instdir}/Flask_Migrate*.egg-info
%{pgadmin4py2instdir}/flask_migrate/*
%endif

%changelog
* Wed May 31 2017 Devrim Gündüz <devrim@gunduz.org> -1:2.0.4-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
