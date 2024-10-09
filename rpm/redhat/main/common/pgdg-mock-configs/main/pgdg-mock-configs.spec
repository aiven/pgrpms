Name:		pgdg-mock-configs
Version:	42.0
Release:	1PGDG%{?dist}
Summary:	PGDG RPM mock core config files basic chroots
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	pgdg-fedora-40-x86_64.cfg
Source1:	pgdg-fedora-all.tpl
BuildArch:	noarch

# distribution-gpg-keys contains GPG keys used by mock configs
Requires:	distribution-gpg-keys >= 1.105 mock-core-configs
# specify minimal compatible version of mock
Requires:	mock >= 5.4.post1
Requires:	mock-filesystem

Requires(post):	coreutils
# to detect correct default.cfg
Requires(post):	python3-dnf
Requires(post):	python3-hawkey
Requires(post):	system-release
Requires(post):	python3
Requires(post):	sed

%description
PGDG mock configuration files which allow you to create chroots for Fedora

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/mock/templates
%{__cp} -a %{SOURCE0} %{buildroot}%{_sysconfdir}/mock
%{__cp} -a %{SOURCE1} %{buildroot}%{_sysconfdir}/mock/templates

%files
%license LICENSE.txt
%doc README.txt
%{_sysconfdir}/mock/pgdg-fedora-40-x86_64.cfg
%{_sysconfdir}/mock/templates/pgdg-fedora-all.tpl

%changelog
* Wed Oct 9 2024 Devrim Gündüz <devrim@gunduz.org> 42.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
