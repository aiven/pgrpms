%global sname paramiko

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
Version:	2.6.0
Release: 	3%{?dist}
Summary:	SSH2 protocol library for python

# No version specified.
License:	LGPLv2+
URL:		https://github.com/paramiko/paramiko
Source0:	%{url}/archive/%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%global paramiko_desc \
Paramiko (a combination of the Esperanto words for "paranoid" and "friend") is\
a module for python 2.3 or greater that implements the SSH2 protocol for secure\
(encrypted and authenticated) connections to remote machines. Unlike SSL (aka\
TLS), the SSH2 protocol does not require hierarchical certificates signed by a\
powerful central authority. You may know SSH2 as the protocol that replaced\
telnet and rsh for secure access to remote shells, but the protocol also\
includes the ability to open arbitrary channels to remote services across an\
encrypted tunnel (this is how sftp works, for example).

%description
%{paramiko_desc}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-bcrypt >= 3.1.3
BuildRequires: python3-cryptography >= 2.5
BuildRequires: python3-pytest
BuildRequires: python3-pytest-mock
Requires:      python3-bcrypt >= 3.1.3
Requires:      python3-cryptography >= 2.5

%prep
%autosetup -p1 -n %{sname}-%{version}

chmod -c a-x demos/*
sed -i -e '/^#!/,1d' demos/*

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-*.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-*.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%license LICENSE
%doc NEWS README.rst
%{pgadmin4py3instdir}/*.egg-info/
%{pgadmin4py3instdir}/%{sname}/*

%changelog
* Sun Sep 29 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-3
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4-python-sshtunnel package for RHEL 8.
