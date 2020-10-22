%global pypi_name Flask-Login
%global sname	flask-login

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-python3-%{sname}
Version:	0.4.1
Release:	2%{?dist}
Summary:	User session management for Flask

License:	MIT
URL:		https://github.com/maxcountryman/flask-login
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
BuildRequires:	python3-devel python3-setuptools
Requires:	pgadmin4-python3-flask
%endif

%description
Flask-Login provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users' sessions over
extended periods of time.

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
%{__mv} %{buildroot}%{python3_sitelib}/flask_login/ %{buildroot}%{python3_sitelib}/Flask_Login-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd

%files
%license LICENSE
%doc README.md
%{pgadmin4py3instdir}/Flask_Login*.egg-info
%{pgadmin4py3instdir}/flask_login*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-2
- Switch to PY3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Update to 0.4.1
- Add RHEL 8 support

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.2-3.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-1
- Update to 0.3.2

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.2.11-3
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency. Spec file taken from Fedora repo.
