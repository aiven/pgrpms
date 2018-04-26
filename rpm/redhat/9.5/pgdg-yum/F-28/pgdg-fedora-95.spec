Name:		pgdg-fedora95
Version:	9.5
Release:	5
Summary:	PostgreSQL 9.5.X PGDG RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-95
Source2:	pgdg-95-fedora.repo
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
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-95

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
* Thu Dec 28 2017 Devrim Gündüz <devrim@gunduz.org> - 9.5-5
- Add separate repo for -debuginfo and -debugsource packages

* Sun Sep 25 2016 Devrim Gündüz <devrim@gunduz.org> - 9.5-4
- Website is now https, per #1742

* Wed Oct 21 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-3
- Point the download URL in repo file to new location.

* Thu Jul 9 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-2
- Re-enable gpgcheck in repo file, per Fedora bugzilla #1239039.

* Fri Jul 3 2015 Devrim Gündüz <devrim@gunduz.org> - 9.5-1
- 9.5 set
