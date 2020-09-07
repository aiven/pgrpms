%global		debug_package %{nil}

%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	A Template for PostgreSQL HA with ZooKeeper, etcd or Consul
Name:		patroni
Version:	2.0.0
Release:	2%{?dist}
License:	MIT
Source0:	https://github.com/zalando/%{name}/archive/v%{version}.tar.gz
Source1:	%{name}.service
URL:		https://github.com/zalando/%{name}

BuildRequires:	python3-setuptools python3-psycopg2 >= 2.5.4

Requires:	python3-cdiff python3-psutil >= 2.0.0
Requires:	python3-psycopg2 >= 2.5.4
Requires:	python3-psutil >= 2.0.0 python3-psycopg2 >= 2.5.4

%if 0%{?rhel} == 7
Requires:	python36-click >= 4.1 python36-six >= 1.7
Requires:	python36-dateutil python36-prettytable >= 0.7
Requires:	python36-PyYAML
%else
Requires:	python3-click >= 4.1 python3-six >= 1.7
Requires:	python3-dateutil python3-prettytable >= 0.7
Requires:	python3-pyyaml
%endif

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
%if 0%{?rhel} == 7
Requires:	python36-dns python36-urllib3 python36-certifi
%else
Requires:	python3-dns python3-urllib3 python3-certifi
%endif

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

# Install sample yml files:
%{__mkdir} -p %{buildroot}%{docdir}/%{name}
%{__cp} postgres0.yml postgres1.yml %{buildroot}%{docdir}/%{name}


# Install unit file:
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# We don't need to ship this file, per upstream:
%{__rm} -f %{buildroot}%{_bindir}/patroni_wale_restore

%post
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{name}.service
   %endif
   %else
   %systemd_post %{name}.service
   %endif
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%doc docs README.rst postgres0.yml postgres1.yml
%attr (755,root,root) %{_bindir}/patroni
%attr (755,root,root) %{_bindir}/patronictl
%attr (755,root,root) %{_bindir}/patroni_raft_controller
%{_unitdir}/%{name}.service
%{python3_sitelib}/%{name}*.egg-info
%dir %{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}/*

%files -n %{name}-aws
%attr (755,root,root) %{_bindir}/patroni_aws

%files -n %{name}-consul

%files -n %{name}-etcd

%files -n %{name}-zookeeper


%changelog
* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Fix another missing dependency (needed by urllib3)

* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0
- Fix missing dependencies, per Alexandre Pereira

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-4
- Fix RHEL 7 dependencies

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-3
- Add unit file, per Hüseyin.
- Install sample config files, per Hüseyin.
- Fix BR and Requires, per Alexander.

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-2
- Add missing requires, per Hüseyin Sönmez.
- Create (meta) subpacakges for consul, etcd, aws and zookeeper,
  per discussion with Hüseyin.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1
- Initial packaging for PostgreSQL RPM repository
