%global sname	pgcenter

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	top-like PostgreSQL statistics viewer.
Name:		pgcenter
Version:	0.3.0
Release:	1%{?dist}.1
License:	BSD
Source0:	https://github.com/lesovsky/%{name}/archive/%{version}.tar.gz
Patch0:		%{name}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/lesovsky/%{name}
Requires:	postgresql%{pgmajorversion}-libs
BuildRequires:	postgresql%{pgmajorversion}, ncurses-devel

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
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
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

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

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 3 2016 - Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0
- Update patch0, and remove portions that are included ino
  upstream.

* Wed Jan 06 2016 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
