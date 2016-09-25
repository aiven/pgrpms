Name:		pgdg-ami201503-96
Version:	9.6
Release:	2
Summary:	PostgreSQL 9.6.X PGDG RPMs for Amazon Linux AMI 2015.03 - Yum Repository Configuration
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-96
Source2:	pgdg-96-ami201503.repo
BuildArch:	noarch
Requires:	system-release

%description
This package contains yum configuration for Amazon Linux AMI 2015.03, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-96

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-96

%files
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Sep 25 2016 Devrim Gündüz <devrim@gunduz.org> - 9.6-2
- Website is now https, per #1742

* Fri Nov 13 2015 Devrim Gündüz <devrim@gunduz.org> - 9.6-1
- Initial set for 9.6
