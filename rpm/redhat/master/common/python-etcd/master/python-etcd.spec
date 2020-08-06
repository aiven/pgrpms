%global modname etcd
%global srcname python-%{modname}

Name:		python3-%{modname}
Version:	0.4.5
Release:	20%{?dist}
Summary:	A python client library for etcd

License:	MIT
URL:		http://pypi.python.org/pypi/%{srcname}
# Using the github URL because the tarball file at pypi excludes
# the license file. But github tarball files are named awkwardly.
Source0:	https://github.com/jplana/%{srcname}/archive/%{version}.tar.gz

BuildArch:	noarch

# See https://bugzilla.redhat.com/1393497
# Also https://fedoraproject.org/wiki/Packaging:Guidelines#Noarch_with_Unported_Dependencies
ExclusiveArch:	noarch %{ix86} x86_64 %{arm} aarch64 ppc64le s390x

%if 0%{?rhel} == 7
BuildRequires:	python36-mock
BuildRequires:	python36-nose
BuildRequires:	python36-pyOpenSSL
%else
BuildRequires:	python3-mock
BuildRequires:	python3-nose
BuildRequires:	python3-pyOpenSSL
%endif

%description
Client library for interacting with an etcd service, providing Python
access to the full etcd REST API. Includes authentication, accessing
and manipulating shared content, managing cluster members, and leader
election.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-20
- Initial packaging for PostgreSQL RPM repository to satisfy
  patroni dependency on RHEL 8
