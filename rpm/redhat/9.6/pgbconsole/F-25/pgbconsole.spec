%global pgmajorversion 96
%global pgpackageversion 9.6
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname	pgbconsole

Summary:	top-like console for Pgbouncer - PostgreSQL connection pooler
Name:		pgbconsole
Version:	0.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/lesovsky/%{name}/archive/v%{version}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		https://github.com/lesovsky/%{name}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}, ncurses-devel

%description
pgbConsole is the top-like console for Pgbouncer - PostgreSQL connection
pooler. Features:

 * top-like interface
 * show information about client/servers connections, pools/databases
   info and statistics.
 * ability to perform admin commands, such as pause, resume, reload and
   others.
 * ability to show log files or edit configuration in local pgbouncers.

%prep
%setup -q
%patch0 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

install -d %{buildroot}%{_bindir}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{_mandir}/man1
install -m 644 doc/*.gz %{buildroot}%{_mandir}/man1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man1/pgbconsole.1.gz
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md COPYRIGHT
%else
%doc README.md
%license COPYRIGHT
%endif

%{_bindir}/%{name}

%changelog
* Sun Nov 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
