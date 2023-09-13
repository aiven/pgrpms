Name:		pgdg-redhat-nonfree-repo
Version:	42.0
Release:	12PGDG
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / CentOS NonFree
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-redhat-nonfree-all.repo
BuildArch:	noarch
Requires:	/etc/redhat-release

%description
This package contains yum configuration for Red Hat Enterprise Linux, CentOS
non-free repository, and also the GPG key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-nonfree

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-12PGDG
- Add v16 repos

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Add v15 repo

* Fri Dec 17 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-10
- Add v14 repo
- Remove 9.6 and 10 repos
- Remove failovermethod parameter from repo file.

* Sat May 8 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-9
- Sign repository metadata to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271
- Rename GPG key, so that it does not conflict with primary repo.

* Sun Sep 27 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-8
- Add missing repos, remove obsoleted repos.

* Thu Sep 17 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-7
- Add v13 stable repo.

* Fri Nov 15 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-6
- Initial configuration for non-free repo
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
