%global sname	pgbconsole

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	top-like console for Pgbouncer - PostgreSQL connection pooler
Name:		pgbconsole%{pgmajorversion}
Version:	0.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/lesovsky/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/lesovsky/%{sname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}, ncurses-devel

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

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
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
	PATH=%{atpath}/bin/:%{atpath}/sbin:$PATH ; export PATH
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__install} -m 644 doc/*.gz %{buildroot}%{_mandir}/man1

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

%{_bindir}/%{sname}

%changelog
* Sun Nov 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
