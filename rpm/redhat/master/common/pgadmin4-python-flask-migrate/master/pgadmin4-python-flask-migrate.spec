%global pypi_name Flask-Migrate
%global sname	flask-migrate

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		pgadmin4-python3-%{sname}
Version:	2.4.0
Release:	2%{?dist}
Summary:	SQLAlchemy database migrations for Flask applications using Alembic

License:	MIT
URL:		https://github.com/miguelgrinberg/%{pypi_name}
Source0:	https://github.com/miguelgrinberg/%{pypi_name}/archive/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} > 27 || 0%{?rhel} >= 8
Requires:	python3-flask
%endif

%if 0%{?rhel} == 7
Requires:	pgadmin4-python3-flask
%endif

%description
Flask-Migrate is an extension that handles SQLAlchemy database migrations
for Flask applications using Alembic. The database operations are
provided as command line arguments for Flask-Script.

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info


%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
pushd %{py3dir}
%{__ospython} setup.py build
popd


%install
pushd %{py3dir}
%{__ospython} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_migrate %{buildroot}%{python3_sitelib}/Flask_Migrate-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd

%files
%license LICENSE
%doc README.md
%{pgadmin4py3instdir}/Flask_Migrate*.egg-info
%{pgadmin4py3instdir}/flask_migrate/*

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-2
- Switch to Python3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1:2.1.1-1
- Update to 2.1.1

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 1:2.0.4-2
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed May 31 2017 Devrim Gündüz <devrim@gunduz.org> -1:2.0.4-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
