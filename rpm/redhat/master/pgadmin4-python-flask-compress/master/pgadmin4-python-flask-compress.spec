%global sname	flask-compress

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/


%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	1.4.0
Release:	1%{?dist}
Summary:	Compress responses in your Flask app with gzip.
License:	MIT
URL:		https://github.com/colour-science/flask-compress
Source0:	https://github.com/colour-science/flask-compress/archive/v%{version}.tar.gz
BuildArch:	noarch


%if 0%{?fedora} > 27
BuildRequires:	python3-flask python3-brotli
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-python3-flask python36-brotli
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-flask pgadmin4-python3-brotli
%endif

%description
Flask-Compress allows you to easily compress your Flask application's
responses with gzip.

The preferred solution is to have a server (like Nginx) automatically
compress the static files for you. If you don't have that option
Flask-Compress will solve the problem for you.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_compress.py %{buildroot}%{python3_sitelib}/__pycache__/flask_compress*  %{buildroot}%{python3_sitelib}/Flask_Compress-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_compress.py* %{buildroot}%{python2_sitelib}/Flask_Compress-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc README.md
%license LICENSE.txt
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*.egg-info/
%{pgadmin4py3instdir}/flask_compress*py*
%{pgadmin4py3instdir}/__pycache__/flask_compress*
%else
%{pgadmin4py2instdir}/*.egg-info/
%{pgadmin4py2instdir}/flask_compress.py*
%endif

%changelog
* Sun Oct 20 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Iniitial packaging for PostgreSQL RPM repository.
