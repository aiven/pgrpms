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

Summary:	HTML minifier for Python
Name:		django-htmlmin
Version:	0.10.0
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/django-htmlmin
Source0:	https://pypi.io/packages/source/d/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
django-html is an HTML minifier for Python, with full support for HTML
5. It supports Django, Flask and many other Python web frameworks. It
also provides a command line tool, that can be used for static websites
or deployment scripts.

%prep
%setup -q -n %{name}-%{version}

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.rst
%{_bindir}/pyminify
%dir %{python2_sitelib}/htmlmin/
%dir %{python2_sitelib}/django_htmlmin-%{version}-py%{py2ver}.egg-info/
%{python2_sitelib}/htmlmin/*
%{python2_sitelib}/django_htmlmin-%{version}-py%{py2ver}.egg-info/*

%if 0%{?with_python3}
%{python3_sitelib}/django_htmlmin-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/django_htmlmin-0.10.0-py3.5.egg-info/top_level.txt
%{python3_sitelib}/htmlmin/*.py
%{python3_sitelib}/htmlmin/__pycache__/*.pyc
%endif

%changelog
* Sat Nov 12 2016 Devrim Gündüz <devrim@gunduz.org> -0.10.0-1
- Update to 0.10.0
- Install PY3 files for Fedora 24+.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> -0.9.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
