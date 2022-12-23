Summary:	A sample database for PostgreSQL
Name:		pagila
Version:	3.1.0
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/devrimgunduz/%{name}
Source0:	https://github.com/devrimgunduz/%{name}/archive/%{name}-v%{version}.tar.gz

Requires:	postgresql-server >= 12.0

BuildArch:	noarch

%global		_pagiladir  %{_datadir}/%{name}

%description
Pagila is a port of the Sakila example database available for MySQL, which was
originally developed by Mike Hillyer of the MySQL AB documentation team. It
is intended to provide a standard schema that can be used for examples in
books, tutorials, articles, samples, etc.

%prep
%setup -q -n %{name}-%{name}-v%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_pagiladir}
%{__install} -m 644 -p *.sql %{buildroot}%{_pagiladir}

%files
%defattr(0644,root,root,0755)
%doc README.md
%dir %{_pagiladir}
%attr(644,root,root) %{_pagiladir}/*.sql

%changelog
* Fri Dec 23 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0, per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v3.1.0

* Thu Jul 28 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0, per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v3.0.0

* Sat Aug 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 20 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0, which is the version that I forked.

* Mon Sep 27 2010 Devrim Gündüz <devrim@gunduz.org> 0.10.1-2
- Apply some minor fixes for new PostgreSQL RPM layout.

* Sat Jun 14 2008 Devrim Gündüz <devrim@gunduz.org> 0.10.1-1
- Update to 0.10.1

* Fri Feb 1 2008 Devrim Gündüz <devrim@gunduz.org> 0.10.0-1
- Initial packaging for Fedora/EPEL
