Name:		pgdg-centos-stream-repo
Version:	42.0
Release:	17
Summary:	PostgreSQL PGDG RPMs- Yum Repository Configuration for CentOS Stream
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-redhat-all.repo
Source3:	pgdg-redhat-all-centos-stream.repo
BuildArch:	noarch
Requires:	/etc/r-release

%description
This package contains yum configuration for CentOS Stream,
and also the GPG key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d

%{__install} -pm 644 %{SOURCE3} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all-centos-stream.repo

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Fri Apr 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17
- Sign repository metadata on RHEL 8+ to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271

* Wed Apr 14 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-16
- CentOS Stream repo rpm.
