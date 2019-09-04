%global sname pg_auto_failover

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Postgres extension and service for automated failover and high-availability
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.3
Release:	1%{dist}
License:	Apache
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{sname}/
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pg_auto_failover is an extension and service for PostgreSQL that monitors and
manages automated failover for a Postgres cluster. It is optimized for
simplicity and correctness and supports Postgres 10 and newer.

We set up one PostgreSQL server as a monitor node as well as a primary and
secondary node for storing data. The monitor node tracks the health of the
data nodes and implements a failover state machine. On the PostgreSQL nodes,
the pg_autoctl program runs alongside PostgreSQL and runs the necessary
commands to configure synchronous streaming replication.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md docs/
%{pginstdir}/bin/pg_autoctl
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/pgautofailover.so
%{pginstdir}/share/extension/pgautofailover--1.0*.sql
%{pginstdir}/share/extension/pgautofailover.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/pgautofailover*.bc
   %{pginstdir}/lib/bitcode/pgautofailover/*.bc
  %endif
 %endif
%endif

%changelog
* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3
- Fix OS versions in Makefile, the distro name in the packages changed.

* Mon Jun 3 2019 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
