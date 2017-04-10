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

%global sname Flask-Security

Name:		python-flask-security
Summary:	Simple security for Flask apps
Version:	1.7.5
Release:	2%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/%{sname}
Source0:	https://pypi.python.org/packages/source/F/%{sname}/%{sname}-%{version}.tar.gz
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Flask-Security quickly adds security features to your Flask application.

%if 0%{?with_python3}
%package -n python3-flask-security
Summary:	Simple security for Flask apps, python3 version

%description -n python3-flask-security
Flask-Security quickly adds security features to your Flask application.
This is the Python3 version.
%endif

%prep
%setup -q -n %{sname}-%{version}
# Remove irrelevant files:
find . -name "*DS_Store*" -exec rm -rf {} \;

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.rst
%dir %{python_sitelib}/flask_security/
%{python2_sitelib}/flask_security/*
%{python2_sitelib}/Flask_Security-%{version}-py%{py2ver}.egg-info/*

%if 0%{?with_python3}
%files -n python3-flask-security
%dir %{python3_sitelib}/flask_security/
%{python3_sitelib}/flask_security/*
%{python3_sitelib}/Flask_Security-%{version}-py%{py3ver}.egg-info/*
%endif

%changelog
* Sat Nov 12 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.5-2
- Install both PY2 and PY3 versions for Fedora 24+. Needed to
  build pgadmin3 docs.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.5-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
