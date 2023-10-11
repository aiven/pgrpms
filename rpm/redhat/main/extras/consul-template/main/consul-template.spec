%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0
%if 0%{?_version:1}
%global		_verstr	%{_version}
%else
%global		_verstr	0.34.0
%endif

# Consul does not provide tarballs for ppc64le:
ExcludeArch:	ppc64le

%ifarch x86_64
%global		tarballarch amd64
%endif
%ifarch aarch64
%global		tarballarch arm64
%endif

Name:		consul-template
Version:	%{_verstr}
Release:	1PGDG%{?dist}
Summary:	consul-template watches a series of templates on the file system, writing new changes when Consul is updated. It runs until an interrupt is received unless the -once flag is specified.

License:	MPLv2.0
URL:		http://www.consul.io
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{tarballarch}.zip
Source1:	%{name}.sysconfig
Source2:	%{name}.service
Source4:	%{name}.json

Requires:	systemd

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

%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/

%pre
getent group consul-template >/dev/null || groupadd -r consul-template
getent passwd consul-template >/dev/null || \
    useradd -r -g consul-template -d /var/lib/consul-template -s /sbin/nologin \
    -c "consul-template user" consul-template
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%dir %attr(750, root, consul-template) %{_sysconfdir}/%{name}.d
%attr(640, root, consul-template) %{_sysconfdir}/%{name}.d/consul-template.json-dist
%dir %attr(750, consul-template, consul-template) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/consul-template

%doc


%changelog
* Wed Oct 11 2023 Devrim Gündüz <devrim@gunduz.org> 0.34.0-1PGDG
- Update to 0.34.0

* Thu Aug 10 2023 Devrim Gündüz <devrim@gunduz.org> 0.33.0-1PGDG
- Update to 0.33.0
- Add PGDG branding

* Thu Jun 15 2023 Devrim Gündüz <devrim@gunduz.org> 0.32.0-3
- Remove support for old distros.

* Tue May 23 2023 Devrim Gündüz <devrim@gunduz.org> 0.32.0-1
- Update to 0.32.0

* Mon Apr 10 2023 Devrim Gündüz <devrim@gunduz.org> 0.31.0-1
- Update to 0.31.0

* Thu Jan 12 2023 Devrim Gündüz <devrim@gunduz.org> 0.30.0-1
- Update to 0.30.0

* Mon Dec 12 2022 Devrim Gündüz <devrim@gunduz.org> 0.29.6-1
- Update to 0.29.6

* Wed Nov 16 2022 Devrim Gündüz <devrim@gunduz.org> 0.29.5-2
- Enable builds on aarch64, and make sure that the package is
  not built on ppc64le.

* Mon Oct 10 2022 Devrim Gündüz <devrim@gunduz.org> 0.29.5-1
- Update to 0.29.5

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> 0.29.2-1
- Update to 0.29.2

* Tue May 31 2022 Devrim Gündüz <devrim@gunduz.org> 0.29.0-1
- Update to 0.29.0

* Fri Mar 11 2022 Devrim Gündüz <devrim@gunduz.org> 0.28.0-1
- Update to 0.28.0

* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> 0.27.1-1
- Update to 0.27.1

* Fri Oct 2 2020 Devrim Gündüz <devrim@gunduz.org> 0.25.1-1
- Update to 0.25.1

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.24.1-1
- Update to 0.24.1

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> 0.20.0-1
- Initial packaging for PostgreSQL RPM Repository
