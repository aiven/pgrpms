%global sname bgw_replstatus

%pgdg_set_llvm_variables

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.3
Release:	3%{?dist}
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/mhagander/%{sname}
Source0:	https://github.com/mhagander/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.12
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.3-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
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
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
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
%if 0%{?isllvm}
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
 %endif
%else
%endif

%changelog
* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> 1.0.3-3
- Use pgdg_set_llvm_variables macro for LLVM related files.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-3
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-2
- Rebuild against PostgreSQL 11.0

* Thu May 18 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Fri Mar 31 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL YUM repository.

