%global pypi_name Flask-Gravatar

%if 0%{?fedora}
%global with_python3 1
%else
# EL doesn't have Python 3
%global with_python3 0
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2	%{__python}
%global python2_sitelib %{python_sitelib}
%endif

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

Summary:	Small extension for Flask to make usage of Gravatar service easy
Name:		python-flask-gravatar
Version:	0.4.2
Release:	1%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/Flask-Gravatar
Source0:	http://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildRequires:	python-setuptools
%if 0%{?with_python3}
Requires:	python3-flask
%else
Requires:	python-flask
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is small and simple integration gravatar into flask.

%if 0%{?with_python3}
%package -n     python3-flask-gravatar
Summary:	Small extension for Flask to make usage of Gravatar service easy
Requires:	python3-flask

%description -n python3-flask-gravatar
This is small and simple integration gravatar into flask.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3

%install
%{__rm} -rf %{buildroot}
%if 0%{?with_python3}
%{__ospython} setup.py install --skip-build --root %{buildroot}
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc CHANGES README.rst
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%dir %{python_sitelib}/flask_gravatar/
%{python_sitelib}/flask_gravatar/*
%{python2_sitelib}/Flask_Gravatar-%{version}-py%{py2ver}.egg-info/*

%if 0%{?with_python3}
%files -n python3-flask-gravatar
%license LICENSE
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
