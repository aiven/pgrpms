%global _ocfroot /usr/lib/ocf

Name:		resource-agents-paf
Version:	2.3.0
Release:	1%{dist}
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
%{__perl} Build.PL --destdir %{buildroot} --install_path bindoc=%{_mandir}/man7 --install_path libdoc=%{_mandir}/man3
%{__perl} Build

%install
%{__rm} -rf %{buildroot}
./Build install
find "%{buildroot}" -type f -name .packlist -delete

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc README.md
%license LICENSE
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_ocfroot}/resource.d/heartbeat/pgsqlms
%{_ocfroot}/lib/heartbeat/OCF_ReturnCodes.pm
%{_ocfroot}/lib/heartbeat/OCF_Directories.pm
%{_ocfroot}/lib/heartbeat/OCF_Functions.pm
%{_datadir}/resource-agents/ocft/configs/pgsqlms

%changelog
* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Fri Feb 8 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1.1
- Rebuild against PostgreSQL 11.0

* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Tue May 30 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Tue May 30 2017 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Fix all rpmlint warnings, and use more macros. This is the initial
  build for PostgreSQL YUM repository.

* Tue Mar 14 2017 Benoit Lobréau <blo.talkto@gmail.com> - 1.1.0-1
- 1.1.0 major release

* Sun Dec 04 2016 Jehan-Guillaume de Rorthais <jgdr@dalibo.com> - 1.1beta1-1
- 1.1_beta1 beta release

* Wed May 25 2016 Jehan-Guillaume de Rorthais <jgdr@dalibo.com> - 1.0.2-1
- 1.0.2 minor release

* Wed Apr 27 2016 Jehan-Guillaume de Rorthais <jgdr@dalibo.com> - 1.0.1-1
- 1.0.1 minor release

* Wed Mar 02 2016 Jehan-Guillaume de Rorthais <jgdr@dalibo.com> 1.0.0-1
- Official 1.0.0 release

* Tue Mar 01 2016 Jehan-Guillaume de Rorthais <jgdr@dalibo.com> 0.99.0-1
- Initial version
