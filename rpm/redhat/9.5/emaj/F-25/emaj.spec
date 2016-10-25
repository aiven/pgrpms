%global debug_package %{nil}
%global sname e-maj

Name:		emaj
Version:	1.3.1
Release:	1%{?dist}
Summary:	A table update logger for PostgreSQL
Group:		Applications/Databases
License:	GPLv2
URL:		http://pgxn.org/dist/%{sname}/
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
E-Maj is a set of PL/pgSQL functions allowing PostgreSQL Database
Administrators to record updates applied on a set of tables, with
the capability to "rollback" these updates to a predefined point
in time.

%prep
%setup -q -n %{sname}-%{version}

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
%{_datadir}/%{name}-%{version}/sql/*.sql
%{_datadir}/%{name}-%{version}/php/*.php

%changelog
* Sat Sep 17 2016 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Mon Jan 4 2016 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Mon Nov 9 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.0-2
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Jan 22 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Mon Jan 7 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Tue Dec 11 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM repository.
