%global sname pagila

Summary:	A sample database for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	2.0.1
Release:	1%{?dist}.1
License:	BSD
URL:		https://github.com/devrimgunduz/%{sname}
Source0:	https://github.com/devrimgunduz/%{sname}/archive/%{version}.tar.gz

Requires:	postgresql%{pgmajorversion}
BuildArch:	noarch

%global		_pagiladir  %{_datadir}/%{name}

%description
Pagila is a port of the Sakila example database available for MySQL, which was
originally developed by Mike Hillyer of the MySQL AB documentation team. It
is intended to provide a standard schema that can be used for examples in
books, tutorials, articles, samples, etc.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_pagiladir}
%{__install} -m 644 -p *.sql %{buildroot}%{_pagiladir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README.md
%dir %{_pagiladir}
%attr(644,root,root) %{_pagiladir}/*.sql

%changelog
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
