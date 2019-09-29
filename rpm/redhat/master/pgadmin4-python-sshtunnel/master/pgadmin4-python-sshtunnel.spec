%global sname sshtunnel

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

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.1.4
Release:	1%{?dist}
Summary:	SSH tunnels to remote server.

License:	MIT
URL:		https://github.com/pahaz/%{sname}
Source0:	https://files.pythonhosted.org/packages/bf/8d/385c7e7c90e17934b3102ad2902e224c27a7173a6a57ef4805dcef8043b1/sshtunnel-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 27
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Requires:	python3-paramiko
%endif

%if 0%{?rhel} == 7
BuildRequires:	python-devel
BuildRequires:	python-setuptools
Requires:	python-paramiko
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Requires:	pgadmin4-python3-paramiko
%endif

%description
Pure python SSH tunnels.

%prep
%setup -q -n %{sname}-%{version}
%{__sed} -i 's/\r//' LICENSE

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython} setup.py build
popd
%else
%{__ospython} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}%{python3_sitelib}/%{sname}-%{version}*-py%{pyver}.egg-info  %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}.py* %{buildroot}%{python2_sitelib}/%{sname}-%{version}*-py%{pyver}.egg-info  %{buildroot}/%{pgadmin4py2instdir}
%endif
%{__rm} %{buildroot}%{_bindir}/%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info*
%{pgadmin4py3instdir}/%{sname}.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}*
%{pgadmin4py3instdir}/%{sname}.cpython*
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info*
%{pgadmin4py2instdir}/%{sname}.py*
%endif

%changelog
* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-1
- Update to 0.1.4
- Remove patch0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 26 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3
- Initial packaging for pgAdmin4 3.1+
