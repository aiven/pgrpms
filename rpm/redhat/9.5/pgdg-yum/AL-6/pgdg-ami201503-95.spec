Name:		pgdg-ami201503-94
Version:	9.5
Release:	1
Summary:	PostgreSQL 9.5.X PGDG RPMs for Amazon Linux AMI 2015.03 - Yum Repository Configuration
License:	BSD
URL:		http://yum.postgresql.org
Source0:	http://yum.postgresql.org/RPM-GPG-KEY-PGDG-94
Source2:	pgdg-94-ami201503.repo
BuildArch:	noarch
Requires:	system-release

%description
This package contains yum configuration for Amazon Linux AMI 2015.03, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-94

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-94

%files
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Fri Jul 3 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-1
- 9.5 set for Amazon Linux AMI 2015.03.
