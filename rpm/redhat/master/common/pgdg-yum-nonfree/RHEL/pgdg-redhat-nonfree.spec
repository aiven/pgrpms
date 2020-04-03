Name:		pgdg-redhat-nonfree-repo
Version:	42.0
Release:	6
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for Red Hat / CentOS NonFree
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-redhat-nonfree-all.repo
BuildArch:	noarch
Requires:	/etc/redhat-release
Obsoletes:	pgdg-centos12 pgdg-redhat12 pgdg-sl12
Obsoletes:	pgdg-centos11 pgdg-redhat11 pgdg-sl11
Obsoletes:	pgdg-centos10 pgdg-redhat10 pgdg-sl10
Obsoletes:	pgdg-centos96 pgdg-redhat96 pgdg-sl96
Obsoletes:	pgdg-centos95 pgdg-redhat95 pgdg-sl95
Obsoletes:	pgdg-centos94 pgdg-redhat94 pgdg-sl94

%description
This package contains yum configuration for Red Hat Enterprise Linux, CentOS
non-free repository, and also the GPG key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
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
