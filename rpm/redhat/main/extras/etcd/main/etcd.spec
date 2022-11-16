%define		_build_id_links none
%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

Name:		etcd
Version:	3.5.5
Release:	2%{?dist}
Summary:	Distributed reliable key-value store
License:	ASL 2.0
URL:		https://github.com/%{name}-io/%{name}
%ifarch x86_64
Source0:	https://github.com/%{name}-io/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-amd64.tar.gz
%endif
%ifarch ppc64le
Source0:	https://github.com/%{name}-io/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-ppc64le.tar.gz
%endif
%ifarch aarch64
Source0:	https://github.com/%{name}-io/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-arm64.tar.gz
%endif

Source1:        %{name}.service
Source2:        %{name}.conf

BuildRequires:	python3-devel
BuildRequires:	systemd-rpm-macros
Requires(pre):	shadow-utils

%description
etcd is a distributed reliable key-value store for the most critical data
of a distributed system, with a focus on being:
- Simple: well-defined, user-facing API (gRPC)
- Secure: automatic TLS with optional client cert authentication
- Fast: benchmarked 10,000 writes/sec
- Reliable: properly distributed using Raft

%prep
%setup -q -n %{name}-v%{version}-linux-amd64

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} etcd etcdctl etcdutl %{buildroot}/%{_bindir}

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__cp} %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf

%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE1} %{buildroot}/%{_unitdir}/

%{__mkdir} -p %{buildroot}/%{_var}/lib/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} \
    -s /sbin/nologin -c "etcd user" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README*
%dir %attr(750, root, root) %{_sysconfdir}/%{name}
%dir %attr(750, etcd, etcd) %{_var}/lib/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/etcd
%attr(755, root, root) %{_bindir}/etcdctl
%attr(755, root, root) %{_bindir}/etcdutl

%changelog
* Wed Nov 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.5-2
- Make sure that we pick up the correct tarball for all supported
  architectures, not a single one.

* Mon Oct 24 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.5-1
- Update to 3.5.5
- Enable v2 protocol by default,  per Alexandre Pereira:
  https://redmine.postgresql.org/issues/7704

* Wed Sep 14 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.4-2
- Make sure that we don't override the config file, per report and
  fix from Matt Baker.
- Create working directory, so that the daemon can start out of the box.

* Thu Aug 18 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.4-1
- Initial packaging for PostgreSQL RPM repository.
