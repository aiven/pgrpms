%global sname bgw_replstatus

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}.2
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/mhagander/%{sname}
Source0:	https://github.com/mhagander/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
bgw_replstatus is a tiny background worker to cheaply report the
replication status of a node. It's intended to be polled by a load
balancer such as haproxy.

When installed, a background worker will be started that listens on a
defined TCP port (configured bgw_replstatus.port). Any connection to
this port will get a TCP response back (no request necessary, response
will be sent immediately on connect) saying either MASTER or STANDBY
depending on the current state of the node. The connection is then
automatically closed.

Using a background worker like this will make polling a lot more light
weight than making a full PostgreSQL connection, logging in, and
checking the status.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md LICENSE
%else
%doc README.md
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu May 18 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Fri Mar 31 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL YUM repository.

