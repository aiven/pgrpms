%global debug_package %{nil}
%global sname	pgcenter

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	top-like PostgreSQL statistics viewer.
Name:		pgcenter
Version:	0.4.0
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/lesovsky/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/lesovsky/%{name}
Requires:	libpq5 >= 10.0
BuildRequires:	libpq5-devel >= 10.0 ncurses-devel pgdg-srpm-macros

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
PostgreSQL provides various statistics which includes information about
tables, indexes, functions and other database objects and their usage.
Moreover, statistics has detailed information about connections, current
queries and database operations (INSERT/DELETE/UPDATE). But most of this
statistics are provided as permanently incremented counters. The
pgcenter provides convenient interface to this statistics and allow
viewing statistics changes in time interval, eg. per second. The
pgcenter provides fast access for database management task, such as
editing configuration files, reloading services, viewing log files and
canceling or terminating database backends (by pid or using state mask).
However if need execute some specific operations, pgcenter can start
psql session for this purposes.

%prep
%setup -q

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md COPYRIGHT
%else
%doc README.md
%license COPYRIGHT
%endif
%{_bindir}/%{name}
%{_datadir}/%{sname}/init-stats-schema-plperlu.sql
%{_datadir}/%{sname}/init-stats-views.sql

%changelog
* Thu Aug 13 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-1
- Update to 0.4.0
- Use libpq5 package as the dependency.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 3 2016 - Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0
- Update patch0, and remove portions that are included ino
  upstream.

* Wed Jan 06 2016 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
