Summary:	PostgreSQL utility for creating a small, sample database from a larger one
Name:		pg_sample
Version:	1.17
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/mla/%{name}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/mla/%{name}
Requires:	postgresql, perl-DBI, perl-DBD-Pg >= 2.0
BuildArch:	noarch

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
%{__install} -m 755 %{name} %{buildroot}%{_bindir}/%{name}
%{__install} -m 644 README.md %{buildroot}%{_docdir}/%{name}

%files
%doc %{_docdir}/%{name}/README.md
%{_bindir}/%{name}

%changelog
* Wed Aug 28 2024 Devrim Gündüz <devrim@gunduz.org> - 1.17-1PGDG
- Update to 1.17 per changes described at:
  https://github.com/mla/pg_sample/releases/tag/1.17

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.16-1PGDG
- Update to 1.16
- Mark package as noarch
- Add PGDG branding

* Wed Apr 12 2023 Devrim Gündüz <devrim@gunduz.org> - 1.13-1
- Update to 1.13

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.12-1
- Update to 1.12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.09-1.1
- Rebuild against PostgreSQL 11.0

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Initial RPM packaging for yum.postgresql.org

