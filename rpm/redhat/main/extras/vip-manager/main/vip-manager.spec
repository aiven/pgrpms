%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

# Upstream does not provide tarballs for ppc64le:
ExcludeArch:	ppc64le

%ifarch x86_64
%global		tarballarch x86_64
%endif
%ifarch aarch64
%global		tarballarch arm64
%endif

Summary:	Manages a virtual IP for Patroni based on state kept in etcd or Consul
Name:		vip-manager
Version:	2.1.0
Release:	1PGDG%{?dist}
License:	BSD2
URL:		https://github.com/cybertec-postgresql/%{name}

Source0:	https://github.com/cybertec-postgresql/%{name}/releases/download/v%{version}/%{name}_%{version}_Linux_%{tarballarch}.tar.gz
Source2:	%{name}.service

BuildRequires:	systemd
Requires:	systemd


%description
Manages a virtual IP for Patroni based on state kept in etcd or Consul

%prep
%setup -q -n %{name}_%{version}_Linux_%{tarballarch}

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} %{name} %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}/
%{__cp} %{name}.yml %{buildroot}/%{_sysconfdir}/%{name}/
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/%{name}

%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(750, root, root) %{_sysconfdir}/%{name}
%attr(640, root, root) %{_sysconfdir}/%{name}/*yml
%dir %attr(750, root, root) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/%{name}
%doc

%changelog
* Tue Jun 20 2023 Devrim Gündüz <devrim@gunduz.org> 1.15.3-1
- Initial packaging for PostgreSQL RPM Repository
