Name:		pgdg-suse-repo
Version:	42.0
Release:	39PGDG
Summary:	PostgreSQL PGDG RPMs - Zypper Repository Configuration for SuSE Enterprise Linux
License:	PostgreSQL
URL:		https://zypp.postgresql.org
Source0:	pgdg-suse-all-sles15.repo
BuildArch:	noarch
Requires:	sles-release

%description
This package contains zypper configuration for SuSE Enterprise Linux.

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/zypp/repos.d

%{__install} -pm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/zypp/repos.d/pgdg-sles-all.repo

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zypp/repos.d/*

%changelog
* Wed Feb 7 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-39PGDG
- The new repo package, that contains all supported distros.
