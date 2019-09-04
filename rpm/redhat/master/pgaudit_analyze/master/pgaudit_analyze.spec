%global debug_package %{nil}
%global	painstdir	/usr/%{name}

Summary:	PostgreSQL Audit Analyzer
Name:		pgaudit_analyze
Version:	1.0.7
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgaudit/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/pgaudit/%{name}

Requires:	perl-Carp

%description
The PostgreSQL Audit extension (pgAudit) provides detailed session and/or
object audit logging via the standard PostgreSQL logging facility. However,
logs are not the ideal place to store audit information. The PostgreSQL Audit
Log Analyzer (pgAudit Analyze) reads audit entries from the PostgreSQL logs
and loads them into a database schema to aid in analysis and auditing.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{painstdir}
%{__cp} -rp lib bin sql %{buildroot}/%{painstdir}/
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{name}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{name}.md
%dir %{painstdir}/lib/
%dir %{painstdir}/bin/
%dir %{painstdir}/sql/
%{painstdir}/lib/*
%{painstdir}/bin/*
%{painstdir}/sql/*

%changelog
* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Initial RPM packaging for PostgreSQL RPM Repository
