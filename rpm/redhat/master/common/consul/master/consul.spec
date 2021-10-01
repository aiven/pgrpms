%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

Name:		consul
Version:	1.10.3
Release:	1%{?dist}
Summary:	Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

License:	MPLv2.0
URL:		http://www.consul.io
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	%{name}.sysconfig
Source2:	%{name}.service
Source3:	%{name}.init
Source4:	%{name}.json
Source5:	%{name}.logrotate

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
BuildRequires:	systemd-units
Requires:	systemd
%else
Requires:	logrotate
%endif
Requires(pre):	shadow-utils


%description
Consul is a tool for service discovery and configuration. Consul is
distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register
themselves and to discover other services via a DNS or HTTP interface.
External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert
operators about any issues in a cluster. The integration with service
discovery prevents routing traffic to unhealthy hosts and enables service
level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic
configuration, feature flagging, coordination, leader election and more.
The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support
any number of regions without complex configuration.

%prep
%setup -q -c

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} consul %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}.d
%{__cp} %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul.json-dist.hcl
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig
%{__cp} %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
%{__mkdir} -p %{buildroot}/%{_initrddir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d
%{__cp} %{SOURCE3} %{buildroot}/%{_initrddir}/consul
%{__cp} %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre
getent group consul >/dev/null || groupadd -r consul
getent passwd consul >/dev/null || \
    useradd -r -g consul -d /var/lib/consul -s /sbin/nologin \
    -c "consul.io user" consul
exit 0

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(750, root, consul) %{_sysconfdir}/%{name}.d
%attr(640, root, consul) %{_sysconfdir}/%{name}.d/consul.json-dist.hcl
%dir %attr(750, consul, consul) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul
%doc

%changelog
* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> 1.30.3-1
- Update to 1.10.3

* Fri Oct 2 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.4-1
- Update to 1.8.4

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.1-1
- Update to 1.8.1
- Disable telemetry.
- Fix config file extension, per Hüseyin Sönmez
- Make sure that consul will restart after a failure, per gripe
  from Hüseyin Sönmez.

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> 1.6.0
- Initial packaging for PostgreSQL RPM Repository
