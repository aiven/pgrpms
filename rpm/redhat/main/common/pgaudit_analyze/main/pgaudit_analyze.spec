%global	painstdir	/usr/%{name}

Summary:	PostgreSQL Audit Analyzer
Name:		pgaudit_analyze
Version:	1.0.8
Release:	2%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgaudit/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/pgaudit/%{name}
BuildArch:	noarch

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 7
Requires:	perl-Carp
%endif

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
* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-2
- Use perl-Carp dependency only on Fedora/RHEL. SLES does not
  have this package, and also it still works.
* Mon Oct 11 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1
- Update to 1.0.8

* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Initial RPM packaging for PostgreSQL RPM Repository
