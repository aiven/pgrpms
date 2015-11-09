%global debug_package %{nil}
Name:		emaj
Version:	1.1.0
Release:	2%{?dist}
Summary:	A table update logger for PostgreSQL
Group:		Applications/Databases
License:	GPLv2
URL:		http://pgfoundry.org/projects/emaj/
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
E-Maj is a set of PL/pgSQL functions allowing PostgreSQL Database
Administrators to record updates applied on a set of tables, with
the capability to "rollback" these updates to a predefined point
in time.

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} -r php sql %{buildroot}%{_datadir}/%{name}-%{version}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES doc LICENSE META.json README
%dir %{_datadir}/%{name}-%{version}
%dir %{_datadir}/%{name}-%{version}/sql
%dir %{_datadir}/%{name}-%{version}/php
%dir %{_datadir}/%{name}-%{version}/sql
%{_datadir}/%{name}-%{version}/sql/*.sql
%{_datadir}/%{name}-%{version}/php/*.php

%changelog
* Mon Nov 9 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.0-2
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Jan 22 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Mon Jan 7 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Tue Dec 11 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM repository.
