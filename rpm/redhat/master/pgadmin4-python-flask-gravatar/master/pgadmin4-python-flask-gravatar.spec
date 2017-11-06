%global pypi_name Flask-Gravatar
%global sname flask-gravatar

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

Summary:	Small extension for Flask to make usage of Gravatar service easy
Version:	0.4.2
Release:	2%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/Flask-Gravatar
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if 0%{?with_python3}
BuildRequires:	python3-setuptools
Requires:	pgadmin4-python3-flask
%else
BuildRequires:	python-setuptools
Requires:	pgadmin4-python-flask
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is small and simple integration gravatar into flask.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_gravatar %{buildroot}%{python3_sitelib}/Flask_Gravatar-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_gravatar %{buildroot}%{python2_sitelib}/Flask_Gravatar-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%if 0%{?with_python3}
%license LICENSE
%doc CHANGES README.rst
%{pgadmin4py3instdir}/Flask_Gravatar*.egg-info
%{pgadmin4py3instdir}/flask_gravatar/*
%else
%doc CHANGES README.rst LICENSE
%{pgadmin4py2instdir}/Flask_Gravatar*.egg-info
%{pgadmin4py2instdir}/flask_gravatar/*
%endif

%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
