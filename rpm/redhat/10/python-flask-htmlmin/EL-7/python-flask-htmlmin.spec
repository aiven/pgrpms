%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global py2ver %(echo `%{__python} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global pkg_name	flask-htmlmin
%global mod_name	Flask-HTMLmin

%if 0%{?with_python3}
Name:		python3-%{pkg_name}
%else
Name:		python-%{pkg_name}
%endif
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

%prep
%setup -q -n %{mod_name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

%files
%doc LICENSE README.md
%if 0%{?with_python3}
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_htmlmin.py
%{python3_sitelib}/__pycache__/flask_htmlmin.cpython-*.pyc
%else
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/flask_htmlmin.py*
%endif

%changelog
* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Initial packaging for pgadmin4.
