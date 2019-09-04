%if 0%{?fedora} > 26
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

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global sname sshtunnel

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
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Requires:	python3-paramiko
%else
BuildRequires:	python-devel
BuildRequires:	python-setuptools
Requires:	python-paramiko
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
%{__ospython3} setup.py build
popd
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}%{python3_sitelib}/%{sname}-%{version}*-py%{py3ver}.egg-info  %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}.py* %{buildroot}%{python2_sitelib}/%{sname}-%{version}*-py%{py2ver}.egg-info  %{buildroot}/%{pgadmin4py2instdir}
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
