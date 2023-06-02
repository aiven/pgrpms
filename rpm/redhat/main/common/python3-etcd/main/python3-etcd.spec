%global modname etcd
%global srcname python-%{modname}

Name:		python3-%{modname}
Version:	0.4.5
Release:	44%{?dist}
Summary:	A python client library for etcd

License:	MIT
URL:		http://pypi.python.org/pypi/%{srcname}
# Using the github URL because the tarball file at pypi excludes
# the license file. But github tarball files are named awkwardly.
Source0:	https://github.com/jplana/%{srcname}/archive/%{version}.tar.gz

BuildArch:	noarch

# See https://bugzilla.redhat.com/1393497
# Also https://fedoraproject.org/wiki/Packaging:Guidelines#Noarch_with_Unported_Dependencies
ExclusiveArch:	noarch %{ix86} x86_64 %{arm} aarch64 ppc64le s390x powerpc64le

%if 0%{?rhel} == 7
Requires:	python36-urllib3 >= 1.7.1
Requires:	python36-dns >= 1.13.0
%endif
%if 0%{?fedora}
Requires:	python3-urllib3 >= 1.7.1
Requires:	python3-dns >= 1.13.0
%endif
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	python3-urllib3 >= 1.7.1
Requires:	python3-dnspython >= 1.13.0
%endif
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
* Fri Jun 2 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-44
- Add SLES 15 support.

* Thu Mar 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-43
- Fix a dependency name

* Wed Sep 21 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-42
- Fix dependencies. The previous one was for tests. Now we specify
  runtime dependencies.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-20
- Initial packaging for PostgreSQL RPM repository to satisfy
  patroni dependency on RHEL 8
