Name:		pgdg-oraclelinux11
Version:	11
Release:	1
Summary:	PostgreSQL 11.X PGDG RPMs for Oracle Linux - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-11
Source2:	pgdg-11-oraclelinux.repo
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
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-11

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
%{__rm} -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-11

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Mar 11 2018 Devrim Gündüz <devrim@gunduz.org> - 11-1
- Initial set for PostgreSQL 11

* Sat Sep 23 2017 Devrim Gündüz <devrim@gunduz.org> - 10-2
- Final modification for v10 Gold.

* Thu Jan 5 2017 Devrim Gündüz <devrim@gunduz.org> - 10-1
- Initial set for PostgreSQL 10

