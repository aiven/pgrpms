Summary:	Break a PostgreSQL dump file into pre-data and post-data segments
Name:		split_postgres_dump
Version:	1.3.3
Release:	2%{?dist}.1
License:	BSD
Source0:	https://github.com/bucardo/Split_postgres_dump/archive/%{version}.tar.gz
Source2:	README.%{name}
URL:		https://github.com/bucardo/Split_postgres_dump
Requires:	perl-Data-Dumper
BuildArch:	noarch

%description
split_postgres_dump is a small Perl script that breaks a --schema-only
dump file into pre and post sections. The pre section contains everything
needed to import the data, while the post section contains those actions
that should be done after the data is loaded, namely the creation of
indexes, constraints, and triggers.

%prep
%setup -q -n Split_postgres_dump-%{version}

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 755 %{buildroot}%{_bindir}
%{__install} -d -m 755 %{buildroot}%{_docdir}/%{name}

%{__install} -m 755 %{name} %{buildroot}%{_bindir}/
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_docdir}/%{name}/README.%{name}

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-2.1
- Rebuild against PostgreSQL 11.0

* Fri Jul 15 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-2
- Spec file cleanup:
 * Remove whitespaces
 * Add Requires: for perl-Data-Dumper
 * Use macros for rm
 * Fix URL

* Mon Apr 8 2013 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
