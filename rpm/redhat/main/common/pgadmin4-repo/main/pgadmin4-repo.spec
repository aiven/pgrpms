Name:		pgadmin4-fedora-repo
Version:	0.9
Release:	1
Summary:	pgAdmin4 repo switch configuration for PGDG - Fedora
License:	PostgreSQL
URL:		https://www.pgadmin.org
Source0:	PGADMIN_PKG_KEY
Source2:	pgadmin4.repo
BuildArch:	noarch
Requires:	/etc/fedora-release

Obsoletes:	pgadmin4 <= 4.30 pgadmin4-docs <= 4.30
Obsoletes:	pgadmin4-web <= 4.30
Obsoletes:	pgadmin4-desktop-common <= 4.30 pgadmin4-desktop-gnome <= 4.30

%description
This package contains yum configuration for Fedora, and also the GPG
key for pgAdmin4.

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/PGADMIN_PKG_KEY

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%post

echo "
pgAdmin4 is removed from PostgreSQL RPM repos. Please use upstream packages.

To install pgAdmin, run one of the following commands:

# Install for both desktop and web modes.
sudo yum install pgadmin4

# Install for desktop mode only.
sudo yum install pgadmin4-desktop

# Install for web mode only.
sudo yum install pgadmin4-web
"

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- The new repo package

