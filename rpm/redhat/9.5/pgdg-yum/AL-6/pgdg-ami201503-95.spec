Name:		pgdg-ami201503-95
Version:	9.5
Release:	3
Summary:	PostgreSQL 9.5.X PGDG RPMs for Amazon Linux AMI 2015.03 - Yum Repository Configuration
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-95
Source2:	pgdg-95-ami201503.repo
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
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-95

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-95

%files
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Sep 25 2016 Devrim Gündüz <devrim@gunduz.org> - 9.5-3
- Website is now https, per #1742

* Wed Oct 21 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-2
- Point the download URL in repo file to new location.

* Fri Jul 3 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-1
- 9.5 set for Amazon Linux AMI 2015.03.
