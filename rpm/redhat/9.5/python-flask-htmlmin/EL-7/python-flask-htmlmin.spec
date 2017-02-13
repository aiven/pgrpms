%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

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


%global pkg_name	flask-htmlmin
%global mod_name	Flask-HTMLmin

Name:		python-%{pkg_name}
Version:	1.2
Release:	1%{?dist}
Summary:	Flask html response minifier
Group:		Development/Libraries
License:	BSD
URL:		https://github.com/hamidfzm/%{mod_name}/
Source0:	https://github.com/hamidfzm/%{mod_name}/archive/v%{version}.tar.gz
BuildArch:	noarch

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{pkg_name}}
%else
%{?python_provide:%python_provide python-%{pkg_name}}
%endif

%description
Minify flask text/html mime types responses. Just add MINIFY_PAGE = True to
your deployment config to minify html and text responses of your flask
application.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:	Flask html response minifier

%description -n python3-%{pkg_name}
Minify flask text/html mime types responses. Just add MINIFY_PAGE = True to
your deployment config to minify html and text responses of your flask
application.
%endif

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%files
%doc LICENSE README.md
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/flask_htmlmin.py*
%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc LICENSE README.md
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_htmlmin.py
%{python3_sitelib}/__pycache__/flask_htmlmin.cpython-*.pyc
%endif

%changelog
* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Initial packaging for pgadmin4.
