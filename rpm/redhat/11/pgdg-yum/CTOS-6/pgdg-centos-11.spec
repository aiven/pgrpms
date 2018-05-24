Name:		pgdg-centos%{pgmajorversion}
Version:	%{pgmajorversion}
Release:	2
Summary:	PostgreSQL %{pgmajorversion}.X PGDG RPMs for CentOS - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-%{pgmajorversion}
Source2:	pgdg-%{pgmajorversion}-centos.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	centos-release

%description
This package contains yum configuration for CentOS, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-%{pgmajorversion}

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
%{__rm} -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-%{pgmajorversion}

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu May 24 2018 Devrim Gündüz <devrim@gunduz.org> - 11-2
- Switch to v11 main repo.

* Sun Mar 11 2018 Devrim Gündüz <devrim@gunduz.org> - 11-1
- Initial set for PostgreSQL 11

* Sat Sep 23 2017 Devrim Gündüz <devrim@gunduz.org> - 10-2
- Final modification for v10 Gold.

* Thu Jan 5 2017 Devrim Gündüz <devrim@gunduz.org> - 10-1
- Initial set for PostgreSQL 10


