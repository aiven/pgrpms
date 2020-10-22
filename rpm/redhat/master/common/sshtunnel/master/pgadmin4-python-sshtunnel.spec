%global sname sshtunnel

%if 0%{?fedora} > 27 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

Name:		pgadmin4-python3-%{sname}
Version:	0.1.4
Release:	2%{?dist}
Summary:	SSH tunnels to remote server.

License:	MIT
URL:		https://github.com/pahaz/%{sname}
Source0:	https://files.pythonhosted.org/packages/bf/8d/385c7e7c90e17934b3102ad2902e224c27a7173a6a57ef4805dcef8043b1/sshtunnel-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} > 27 || 0%{?rhel} >= 8
Requires:	python3-paramiko
%endif

%if 0%{?rhel} == 7
Requires:	python36-paramiko
%endif

%description
Pure python SSH tunnels.

%prep
%setup -q -n %{sname}-%{version}
%{__sed} -i 's/\r//' LICENSE

%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}

%build
pushd %{py3dir}
%{__ospython} setup.py build
popd

%install
%{__rm} -rf %{buildroot}

pushd %{py3dir}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}%{python3_sitelib}/%{sname}-%{version}*-py%{pyver}.egg-info  %{buildroot}/%{pgadmin4py3instdir}
popd
%{__rm} %{buildroot}%{_bindir}/%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{pgadmin4py3instdir}/*%{sname}*.egg-info*
%{pgadmin4py3instdir}/%{sname}.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}*
%{pgadmin4py3instdir}/%{sname}.cpython*

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-2
- Switch to PY3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-1
- Update to 0.1.4
- Remove patch0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 26 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3
- Initial packaging for pgAdmin4 3.1+
