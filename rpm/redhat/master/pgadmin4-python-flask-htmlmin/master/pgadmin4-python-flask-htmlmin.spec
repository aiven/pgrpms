%global sname	flask-htmlmin
%global mod_name	Flask-HTMLmin

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
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

Version:	1.5.0
Release:	1%{?dist}
Summary:	Flask html response minifier
License:	BSD
URL:		https://github.com/hamidfzm/%{mod_name}/
Source0:	https://github.com/hamidfzm/%{mod_name}/archive/v%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} > 27
BuildRequires:	python3-devel python3-setuptools
Requires:	python3-htmlmin
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
Requires:	pgadmin4-python-htmlmin
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-devel python3-setuptools
Requires:	pgadmin4-python3-htmlmin
%endif

%description
Minify flask text/html mime types responses. Just add MINIFY_PAGE = True to
your deployment config to minify html and text responses of your flask
application.

%prep
%setup -q -n %{mod_name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_htmlmin/ %{buildroot}%{python3_sitelib}/Flask_HTMLmin-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%{__rm} -f %{buildroot}/%{pgadmin4py3instdir}/__init__*.pyc
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_htmlmin/  %{buildroot}%{python2_sitelib}/Flask_HTMLmin-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc LICENSE README.md
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Flask_HTMLmin*.egg-info/
%{pgadmin4py3instdir}/flask_htmlmin/*.py
%{pgadmin4py3instdir}/flask_htmlmin/__pycache__/
%else
%{pgadmin4py2instdir}/Flask_HTMLmin*.egg-info/
%{pgadmin4py2instdir}/flask_htmlmin/*.py*
%endif

%changelog
* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2

* Sat Apr 7 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-6
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Tue Feb 27 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-5
- Require our own python-htmlmin package.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1.2-4
- Move the components under pgadmin web directory, per #2332.

* Fri Feb 17 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-3
- Another attempt to fix python3-htmlmin dependency on Fedora 24+

* Fri Feb 17 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-2
- Bump up package version for python-htmlmin dependency.

* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Initial packaging for pgadmin4.
