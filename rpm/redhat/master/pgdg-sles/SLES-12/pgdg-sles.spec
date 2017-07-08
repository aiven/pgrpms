Name:		pgdg-sles12
Version:	1.0
Release:	1
Summary:	PostgreSQL PGDG RPMs for SLES - Zypper Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-10
Source2:	pgdg-sles.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	sles-release

%description
This package contains yum configuration for SLES 12 , and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-10

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/zypp/repos.d
%{__install} -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/zypp/repos.d/

%clean
%{__rm} -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-10

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/zypp/repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sat Jul 8 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial set for SLES 12

