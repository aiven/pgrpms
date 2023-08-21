%global sname pldebugger

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
Version:	1.5
Release:	3PGDG%{?dist}
Summary:	PL/pgSQL debugger server-side code
License:	Artistic 2.0
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
Source1:	%{sname}.LICENSE

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.3-1
Provides:	%{sname}%{pgmajorversion} = %{version}

%description
This module is a set of shared libraries which implement an API for
debugging PL/pgSQL functions on PostgreSQL 9.4 and above. The pgAdmin
project (http://www.pgadmin.org/) provides a client user interface as
part of pgAdmin 4.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pldebugger
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pldebugger
%endif

%prep
%setup -q -n %{sname}-%{version}

%{__cp} -p %{SOURCE1} ./LICENSE

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 README.%{sname} %{buildroot}%{pginstdir}/doc/extension/README.%{sname}

%files
%doc %{pginstdir}/doc/extension/README.%{sname}
%license LICENSE
%{pginstdir}/lib/plugin_debugger.so
%{pginstdir}/share/extension/pldbgapi*.sql
%{pginstdir}/share/extension/pldbgapi*.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/plugin_debugger*.bc
 %{pginstdir}/lib/bitcode/plugin_debugger/*.bc
%endif

%changelog
* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-3PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Oct 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5

* Tue Oct 12 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4-2
- Provide non-underscore version as well, in order not to break
  upgrades and existing scripts. Per Dave Page and others.

* Thu Sep 23 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3
- Switch to the new URL

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jun 5 2017 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL YUM repository.

