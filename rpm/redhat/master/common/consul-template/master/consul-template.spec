%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0
%if 0%{?_version:1}
%global		_verstr	%{_version}
%else
%global		_verstr	0.24.1
%endif

Name:		consul-template
Version:	%{_verstr}
Release:	1%{?dist}
Summary:	consul-template watches a series of templates on the file system, writing new changes when Consul is updated. It runs until an interrupt is received unless the -once flag is specified.

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
consul-template watches a series of templates on the file system, writing
new changes when Consul is updated. It runs until an interrupt is received
unless the -once flag is specified.

%prep
%setup -q -c

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} consul-template %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}.d
%{__cp} %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul-template.json-dist
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig
%{__cp} %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
%{__mkdir} -p %{buildroot}/%{_initrddir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d
%{__cp} %{SOURCE3} %{buildroot}/%{_initrddir}/consul-template
%{__cp} %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre
getent group consul-template >/dev/null || groupadd -r consul-template
getent passwd consul-template >/dev/null || \
    useradd -r -g consul-template -d /var/lib/consul-template -s /sbin/nologin \
    -c "consul-template user" consul-template
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
%dir %attr(750, root, consul-template) %{_sysconfdir}/%{name}.d
%attr(640, root, consul-template) %{_sysconfdir}/%{name}.d/consul-template.json-dist
%dir %attr(750, consul-template, consul-template) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul-template

%doc


%changelog
* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.24.1-1
- Update to 0.24.1

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> 0.20.0-1
- Initial packaging for PostgreSQL RPM Repository
