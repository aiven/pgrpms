Name:		pgdg-oraclelinux91
Version:	9.1
Release:	7
Summary:	PostgreSQL 9.1.X PGDG RPMs for Oracle Linux - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		http://yum.postgresql.org
Source0:	http://yum.postgresql.org/RPM-GPG-KEY-PGDG-91
Source2:	pgdg-91-oraclelinux.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	oraclelinux-release

%description
This package contains yum configuration for Oracle Linux, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-91

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-91

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Wed Oct 21 2015 Devrim Gündüz <devrim@gunduz.org> - 9.1-7
- Point the download URL in repo file to new location.

* Tue Apr 29 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.1-6
- Initial support for Oracle Linux 6.
