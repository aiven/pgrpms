Name:		pgdg-redhat-repo
Version:	42.0
Release:	12
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / CentOS on aarch64
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-AARCH64
Source2:	pgdg-redhat-all.repo
BuildArch:	noarch
Requires:	/etc/redhat-release

%description
This package contains yum configuration for Red Hat Enterprise Linux, CentOS,
and also the GPG key for PGDG RPMs on aarch64.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-AARCH64

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-12
- Fix v13 debug repo URL, per report from Justin Pryzby.

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Initial repo package for the PostgreSQL YUM aarch64 repository.
