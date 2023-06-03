%global sname bgw_replstatus

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.6
Release:	2%{?dist}.1
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/mhagander/%{sname}
Source0:	https://github.com/mhagander/%{sname}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.12
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.3-2

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

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for bgw_replstatus
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for bgw_replstatus
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jul 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-1
- Update to 1.0.6
- Split llvmjit package
- Remove superfluous %%clean section.

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

