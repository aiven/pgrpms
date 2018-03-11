Name:		pgdg-fedora11
Version:	11
Release:	1
Summary:	PostgreSQL 11.X PGDG RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-11
Source2:	pgdg-11-fedora.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
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

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Mar 11 2018 Devrim Gündüz <devrim@gunduz.org> - 11-1
- Initial set for PostgreSQL 11

* Thu Dec 28 2017 Devrim Gündüz <devrim@gunduz.org> - 10-4
- Add separate repo for -debuginfo and -debugsource packages

* Sat Sep 23 2017 Devrim Gündüz <devrim@gunduz.org> - 10-3
- Final modification for v10 Gold.
- Re-enable GPG checks for Fedora 25 and Fedora 26.

* Sat Mar 25 2017 Devrim Gündüz <devrim@gunduz.org> - 10-2
- Disable gpg checks for Fedora 25, until I can find a way to automate
  package signing.

* Thu Jan 5 2017 Devrim Gündüz <devrim@gunduz.org> - 10-1
- Initial set for PostgreSQL 10
