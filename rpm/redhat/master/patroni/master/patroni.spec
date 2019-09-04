%global debug_package %{nil}

%if  0%{?rhel} && 0%{?rhel} >= 8 || 0%{?fedora} > 23
%global with_python3 1
BuildRequires:	python3-boto python3-urllib3 >= 1.19.1 python3-psycopg2
BuildRequires:	python3-pyyaml python3-requests python3-six >= 1.7
BuildRequires:	python3-kazoo >= 1.3.1 python3-etcd >= 0.4.3
BuildRequires:	python3-prettytable >= 0.7 python3-click
BuildRequires:	python3-tzlocal python3-dateutil python3-psutil >= 2.0.0
#TODO:		python3-consul >= 0.7.0 kubernetes >= 2.0.0
%else
%global with_python3 0
BuildRequires:	python2-boto python2-urllib3 >= 1.19.1 python2-psycopg2
BuildRequires:	python2-pyyaml python2-requests python2-six >= 1.7
BuildRequires:	python2-kazoo >= 1.3.1 python2-etcd >= 0.4.3
BuildRequires:	python2-prettytable >= 0.7 python2-click
BuildRequires:	python2-tzlocal python2-dateutil python2-psutil >= 2.0.0
#TODO:		python3-consul >= 0.7.0 kubernetes >= 2.0.0
%endif

%{expand: %%global pyver %(python2 -c 'import sys;print(sys.version[0:3])')}
%if  0%{?rhel} && 0%{?rhel} <= 7
# Python major version.
%global __ospython %{_bindir}/python2
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if 0%{?suse_version} >= 1315
%global __ospython %{_bindir}/python2
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if 0%{?with_python3}
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif # with_python3

Summary:	https://github.com/zalando/patroni/archive/v1.5.6.tar.gz
Name:		patroni
Version:	1.5.6
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/zalando/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/zalando/%{name}

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
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE docs/
%else
%license LICENSE
%doc docs
%endif
%{_bindir}/patroni
%{_bindir}/patroni_aws
%{_bindir}/patroni_wale_restore
%{_bindir}/patronictl

%if 0%{?with_python3}
%{python3_sitelib}/%{name}*.egg-info
%dir %{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}/*
%else
%{python2_sitelib}/%{name}*.egg-info
%dir %{python2_sitelib}/%{name}/
%dir %{python2_sitelib}/%{name}/*
%endif

%changelog
* Fri Feb 8 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.6-1
- Update to 1.5.6
