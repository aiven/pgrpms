%global _ocfroot /usr/lib/ocf

Name:		resource-agents-paf
Version:	1.1.0
Release:	1%{dist}.1
Summary:	PostgreSQL resource agent for Pacemaker
License:	PostgreSQL
Url:		https://clusterlabs.github.io/PAF/
Source0:	https://github.com/ClusterLabs/PAF/archive/v%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	resource-agents perl perl-Module-Build

%description
PostgreSQL resource agent for Pacemaker.

%prep
%setup -q -n PAF-%{version}

%build
%{__perl} Build.PL --destdir %{buildroot} --install_path bindoc=%{_mandir}/man1 --install_path libdoc=%{_mandir}/man3
%{__perl} Build

%install
%{__rm} -rf %{buildroot}
./Build install

find %{buildroot} -type f -name .packlist -exec rm -f {} +

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc README.md LICENSE
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_ocfroot}/resource.d/heartbeat/pgsqlms
%{_ocfroot}/lib/heartbeat/OCF_ReturnCodes.pm
%{_ocfroot}/lib/heartbeat/OCF_Directories.pm
%{_ocfroot}/lib/heartbeat/OCF_Functions.pm
%{_datadir}/resource-agents/ocft/configs/pgsqlms

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 25 2017 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Package 1.1.0 for RHEL 6.
