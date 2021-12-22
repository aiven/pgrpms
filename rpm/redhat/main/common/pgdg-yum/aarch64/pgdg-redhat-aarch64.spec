Name:		pgdg-redhat-repo
Version:	42.0
Release:	18
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / CentOS on aarch64
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-AARCH64
Source2:	pgdg-redhat-all.repo
Source3:	pgdg-redhat-all-rhel8.repo
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

%if 0%{?rhel} && 0%{?rhel} == 8
%{__install} -pm 644 %{SOURCE3} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all.repo
%else
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/
%endif

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-18
- Add v14 stable repo.

* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17
- Add v15 testing repo.

* Fri Apr 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-16
- Sign repository metadata on RHEL 8+ to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-15
- Remove 9.5 repo

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-14
- Add v14 testing repo.
- Remove 9.4 repo

* Sun Sep 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-13
- Add v13 stable repo.

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-12
- Fix v13 debug repo URL, per report from Justin Pryzby.

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Initial repo package for the PostgreSQL YUM aarch64 repository.
