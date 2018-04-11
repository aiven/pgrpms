%global sname linecache2

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
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
Version:	1.0.0
Release:	14%{?dist}
Summary:	Backport of the linecache module

License:	Python
URL:		https://github.com/testing-cabal/%{sname}
Source0:	https://github.com/testing-cabal/%{sname}/archive/%{version}.tar.gz

BuildArch:	noarch
%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
BuildRequires:	python3-pbr
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-setuptools pgadmin4-python3-pbr
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools python-pbr
%endif

%global _description\
A backport of linecache to older supported Pythons.\

%description %_description

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/linecache2 %{buildroot}%{python3_sitelib}/linecache2-%{version}.dev*-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/linecache2 %{buildroot}%{python2_sitelib}/linecache2-%{version}.dev*-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
# license not shipped by upstream
%if 0%{?with_python3}
%{pgadmin4py3instdir}/linecache2*.egg-info
%{pgadmin4py3instdir}/linecache2/*
%else
%{pgadmin4py2instdir}/linecache2*.egg-info
%{pgadmin4py2instdir}/linecache2/*
%endif


%changelog
* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-14
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.


