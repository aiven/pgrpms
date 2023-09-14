Name:		pgdg-redhat-repo
Version:	42.0
Release:	34PGDG
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / Rocky on aarch64
License:	PostgreSQL
URL:		https://yum.postgresql.org
%if 0%{?rhel} && 0%{?rhel} == 9
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-AARCH64-RHEL9
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-AARCH64-RHEL8
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-AARCH64-RHEL7
%endif
Source2:	pgdg-redhat-all-rhel7-aarch64.repo
Source3:	pgdg-redhat-all-rhel8-aarch64.repo
Source4:	pgdg-redhat-all-rhel9-aarch64.repo
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

%if 0%{?rhel} && 0%{?rhel} == 7
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all.repo
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
%{__install} -pm 644 %{SOURCE3} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all.repo
%endif
%if 0%{?rhel} && 0%{?rhel} == 9
%{__install} -pm 644 %{SOURCE4} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all.repo
%endif

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Tue Sep 12 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-34PGDG
- Add v16 repos
- Remove v16 repos from RHEL 7

* Mon Aug 14 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-33PGDG
- Introduce PostgreSQL 17 testing repo
- Add PGDG branding
- Add missing v16 repos

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-32
- Add pgdg16-source-updates-testing repo.

* Thu Nov 10 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-31
- Keys on RHEL 7 is diferrent from others, so make sure that RHEL
  9 and 8 keys are installed correctly.

* Mon Oct 17 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-30
- Add missing srpm and debuginfo repositories, per report from
  Justin Pryzby.
- Remove 9.6 repos

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-29
- Add v15 stable repo.

* Wed Aug 24 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-28
- Update key, the previous one expired.

* Wed Aug 10 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-27
- Introduce PostgreSQL 16 testing repo

* Wed Mar 30 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-26
- Bump up release number -- I think I pushed wrong repo package
  to the aarch64 repos.

* Wed Mar 16 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-25
- Introduce new repos: pgdg-rhel8-extras and pgdg-rhel9-extras

* Tue Mar 1 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-24
- Fix repo signature error caused by errorneous push to the repo.
- Change -debuginfo repo names, so that yum/dnf will be able
  to pick up these repos automagically with debuginfo-install
  (RHEL 7), and dnf debuginfo-install (on RHEL 8 and 9).
- Add RHEL 9 repo.
- Add missing v14 debuginfo repos, per Demur Rumed.

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
