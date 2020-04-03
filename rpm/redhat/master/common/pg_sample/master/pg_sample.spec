%global debug_package %{nil}

Summary:	PostgreSQL utility for creating a small, sample database from a larger one
Name:		pg_sample
Version:	1.09
Release:	1%{?dist}.1
License:	BSD
Source0:	https://github.com/mla/pg_sample/archive/v1.09.tar.gz
URL:		https://github.com/mla/pg_sample
Requires:	postgresql, perl-DBI, perl-DBD-Pg >= 2.0

%description
pg_sample is a utility for exporting a small, sample dataset from a
larger PostgreSQL database. The output and command-line options closely
resemble the pg_dump backup utility (although only the plain-text format
is supported).

The sample database produced includes all tables from the original,
maintains referential integrity, and supports circular dependencies.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_docdir}/%{name}
%{__install} -m 755 pg_sample %{buildroot}%{_bindir}/%{name}
%{__install} -m 644 README.md %{buildroot}%{_docdir}/%{name}

%files
%doc %{_docdir}/%{name}/README.md
%{_bindir}/%{name}

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.09-1.1
- Rebuild against PostgreSQL 11.0

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Initial RPM packaging for yum.postgresql.org
