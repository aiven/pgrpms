%global		debug_package %{nil}

%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	A Template for PostgreSQL HA with ZooKeeper, etcd or Consul
Name:		patroni
Version:	1.6.5
Release:	2%{?dist}
License:	MIT
Source0:	https://github.com/zalando/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/zalando/%{name}

BuildRequires:	python3-setuptools python3-urllib3 >= 1.19.1 python3-boto
BuildRequires:	python3-pyyaml python3-six >= 1.7
BuildRequires:	python3-kazoo >= 1.3.1 python3-etcd >= 0.4.3
BuildRequires:	python3-consul >= 0.7.1 python3-click >= 4.1
BuildRequires:	python3-prettytable >= 0.7 python3-dateutil
BuildRequires:	python3-psutil >= 2.0.0 python3-cdiff
BuildRequires:	python3-psycopg2 >= 2.5.4

Requires:	python3-cdiff python3-psutil >= 2.0.0 python3-click >= 4.1
Requires:	python3-psycopg2 >= 2.5.4

%description
Patroni is a template for you to create your own customized,
high-availability solution using Python and - for maximum accessibility - a
distributed configuration store like ZooKeeper, etcd, Consul or Kubernetes.
Database engineers, DBAs, DevOps engineers, and SREs who are looking to
quickly deploy HA PostgreSQL in the datacenter-or anywhere else-will
hopefully find it useful.

We call Patroni a "template" because it is far from being a
one-size-fits-all or plug-and-play replication system. It will have its own
caveats. Use wisely.

%package -n %{name}-consul
Summary:	Related components to use patroni with Consul
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-consul >= 0.7.1 consul

%description -n  %{name}-consul
Meta package to pull consul related dependencies for patroni

%package -n %{name}-etcd
Summary:	Related components to use patroni with etcd
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-etcd >= 0.4.3

%description -n  %{name}-etcd
Meta package to pull etcd related dependencies for patroni

%package -n %{name}-aws
Summary:	Related components to use patroni on AWS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-boto

%description -n  %{name}-aws
Meta package to pull AWS related dependencies for patroni

%package -n %{name}-zookeeper
Summary:	Related components to use patroni with Zookeeper
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-kazoo >= 1.3.1

%description -n  %{name}-zookeeper
Meta package to pull zookeeper related dependencies for patroni

%prep
%setup -q
%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root %{buildroot} -O1 --skip-build

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%doc docs README.rst
%attr (755,root,root) %{_bindir}/patroni
%attr (755,root,root) %{_bindir}/patroni_aws
%attr (755,root,root) %{_bindir}/patroni_wale_restore
%attr (755,root,root) %{_bindir}/patronictl

%{python3_sitelib}/%{name}*.egg-info
%dir %{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}/*

%files -n %{name}-aws

%files -n %{name}-consul

%files -n %{name}-etcd

%files -n %{name}-zookeeper


%changelog
* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-2
- Add missing requires, per Hüseyin Sönmez.
- Create (meta) subpacakges for consul, etcd, aws and zookeeper,
  per discussion with Hüseyin.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1
- Initial packaging for PostgreSQL RPM repository
