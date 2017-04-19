%global pypi_name Flask-Login
%global sname	flask-login

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
Version:	0.3.2
Release:	1%{?dist}
Summary:	User session management for Flask

License:	MIT
URL:		https://github.com/maxcountryman/flask-login
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:	noarch

%if %{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%else
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
%endif

%if %{?with_python3}
Requires:	pgadmin4-python3-flask
%else
Requires:	pgadmin4-python-flask
%endif

%description
Flask-Login provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users' sessions over
extended periods of time.

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
%{__mv} %{buildroot}%{python3_sitelib}/__pycache__/flask* %{buildroot}%{python3_sitelib}/flask_login.py %{buildroot}%{python3_sitelib}/Flask_Login-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_login.py* %{buildroot}%{python2_sitelib}/Flask_Login-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?with_python3}
%doc README.md
%license LICENSE
%{pgadmin4py3instdir}/Flask_Login*.egg-info
%{pgadmin4py3instdir}/__pycache__/flask_login*
%{pgadmin4py3instdir}/flask_login*
%else
%doc README.md LICENSE
%{pgadmin4py2instdir}/Flask_Login*.egg-info
%{pgadmin4py2instdir}/flask_login*
%endif


%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-1
- Update to 0.3.2

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.2.11-3
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency. Spec file taken from Fedora repo.
