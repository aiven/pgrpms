Name:		pgdg-sl95
Version:	9.5
Release:	3
Summary:	PostgreSQL 9.5.X PGDG RPMs for Scientific Linux - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-95
Source2:	pgdg-95-sl.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	sl-release

%description
This package contains yum configuration for RHEL, and also the GPG
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

%clean
rm -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-95

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Sep 25 2016 Devrim Gündüz <devrim@gunduz.org> - 9.5-3
- Website is now https, per #1742

* Wed Oct 21 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-2
- Point the download URL in repo file to new location.

* Fri Jul 3 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.5-1
- 9.5 set
