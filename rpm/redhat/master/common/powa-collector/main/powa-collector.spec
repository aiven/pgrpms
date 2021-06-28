%global sname powa_collector

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		powa-collector
Version:	1.1.1
Release:	1%{?dist}
Summary:	POWA data collector daemon

License:	BSD
URL:		https://github.com/powa-team/%{name}
Source0:	https://github.com/powa-team/%{name}/archive/%{version}.tar.gz
Source1:	%{name}.service

BuildRequires:	python3-devel python3-setuptools
Requires:	python3-psycopg2

BuildArch:	noarch

%description
This is a simple multi-threaded python program that performs the
snapshots for all the remote servers configured in a powa repository
database (in the powa_servers table).

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Install sample config file:
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -m 644 powa-collector.conf-dist %{buildroot}%{_sysconfdir}/

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
%service_add_pre %{name}.service
%endif
%else
%systemd_post %{name}.service
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}.py
%{_sysconfdir}/%{name}.conf-dist
%{_unitdir}/%{name}.service
%dir %{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info/*
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.py*

%changelog
* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Thu Oct 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM repository.
