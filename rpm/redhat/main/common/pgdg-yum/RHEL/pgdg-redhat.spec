Name:		pgdg-redhat-repo
Version:	42.0
Release:	23
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / CentOS
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-redhat-all-rhel7.repo
Source3:	pgdg-redhat-all-rhel8.repo
Source4:	pgdg-redhat-all-rhel9.repo
BuildArch:	noarch
Requires:	/etc/redhat-release
Obsoletes:	pgdg-centos12 <= 42.0 pgdg-redhat12 <= 42.0 pgdg-sl12 <= 42.0
Obsoletes:	pgdg-centos11 <= 42.0 pgdg-redhat11 <= 42.0 pgdg-sl11 <= 42.0
Obsoletes:	pgdg-centos10 <= 42.0 pgdg-redhat10 <= 42.0 pgdg-sl10 <= 42.0
Obsoletes:	pgdg-centos96 <= 42.0 pgdg-redhat96 <= 42.0 pgdg-sl96 <= 42.0

%description
This package contains yum configuration for Red Hat Enterprise Linux, CentOS,
and also the GPG key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

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
* Tue Nov 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-23
- Change -debuginfo repo names, so that yum/dnf will be able
  to pick up these repos automagically with debuginfo-install
  (RHEL 7), and dnf debuginfo-install (on RHEL 8 and 9).
- Rename Source3

* Wed Nov 3 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-22
- Add RHEL 9 repo.

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-21
- Add missing v14 debuginfo repos, per Demur Rumed.

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-20
- Add v14 stable repo.

* Thu Jul 15 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-19
- Remove deprecated "failovermethod" parameter from RHEL 8 repo
  config file.

* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-18
- Add v15 testing repo

* Tue Jun 22 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17.2
- Remove obsoletes for 9.5 and 9.4.

* Thu May 6 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17.1
- Sign repository metadata also on RHEL 7.

* Fri Apr 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17
- Sign repository metadata on RHEL 8+ to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-16
- Remove 9.5 repo

* Fri Nov 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-15
- Add a (hopefully temporary) repo to RHEL 8, which supplies
  latest-ish LLVM and CLANG, so that we can respond breakages
  between RHEL 8.n and CentOS 8.n-1, which breaks our llvmjit
  package.

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-14
- Add v14 testing repo.
- Remove 9.4 repo

* Sun Sep 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-13
- Add v13 stable repo.

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-12
- Fix v13 debug repo URL, per report from Justin Pryzby.

* Tue Apr 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Disable 9.4 repo

* Sat Apr 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-10
- Remove duplicate srpm repo, and sync with Fedora repo file (a bit)

* Fri Apr 3 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-9
- Introduce "common" repository.

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-8
- Fix typo in repo file

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-7
- Add debuginfo repos.

* Sat Dec 28 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-6
- Do not replace repo config file after each update. Per #4905

* Wed Sep 25 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-5
- Enable v12 stable repo, and improve description of repo names.
- Drop support for Scientific Linux (project discontinued)
- Add v13 testing repo, and make repo files more consistent with RHEL ones.

* Wed Apr 17 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-4
- Remove major version from GPG file name in the repo file as well.

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-3
- Remove major version from GPG file name, per various reports.

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-2
- Disable v12 testing repo, it is still in development phase. Per Dave Page.

* Wed Apr 10 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0
- The new repo package, that contains all supported distros.
