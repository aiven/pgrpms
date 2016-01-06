%global pgmajorversion 95
%global pgpackageversion 9.5
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname	pgcenter

Summary:	top-like PostgreSQL statistics viewer.
Name:		%{sname}%{pgmajorversion}
Version:	0.2.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/lesovsky/%{sname}/archive/0.2.0.tar.gz
Patch0:		%{sname}-pgxs.patch
URL:		https://github.com/lesovsky/%{sname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	postgresql%{pgöajorversion}-libs
BuildRequires:	postgresql%{pgöajorversion}, ncurses-devel

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
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license COPYRIGHT
%{_bindir}/%{sname}

%changelog
* Tue Apr 27 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.9.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
