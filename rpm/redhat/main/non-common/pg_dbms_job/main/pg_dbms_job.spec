%global debug_package %{nil}
%global sname	pg_dbms_job

Summary:	PostgreSQL extension to schedules and manages jobs in a job queue similar to Oracle DBMS_JOB package
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/MigOpsRepos/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		https://github.com/MigOpsRepos/%{sname}/

%description
This PostgreSQL extension provided full compatibility with the DBMS_JOB
Oracle module.

It allows to manage scheduled jobs from a job queue or to execute immediately
jobs asynchronously. A job definition consist on a code to execute, the next
date of execution and how often the job is to be run. A job runs a SQL
command, plpgsql code or an existing stored procedure.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{sname}/%{sname}.conf.dist
%{pginstdir}/bin/%{sname}
%{pginstdir}/doc/extension/README.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
