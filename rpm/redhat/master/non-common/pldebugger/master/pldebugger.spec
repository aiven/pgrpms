%global sname pldebugger

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.4
Release:	1%{?dist}
Summary:	PL/pgSQL debugger server-side code
License:	Artistic  2.0
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
Source1:	%{sname}.LICENSE

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.3-1

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This module is a set of shared libraries which implement an API for
debugging PL/pgSQL functions on PostgreSQL 9.4 and above. The pgAdmin
project (http://www.pgadmin.org/) provides a client user interface as
part of pgAdmin 4.

%prep
%setup -q -n %{sname}-%{version}

%{__cp} -p %{SOURCE1} ./LICENSE

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 README.%{sname} %{buildroot}%{pginstdir}/doc/extension/README.%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README.%{sname}
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README.%{sname}
%license LICENSE
%endif
%{pginstdir}/lib/plugin_debugger.so
%{pginstdir}/share/extension/pldbgapi*.sql
%{pginstdir}/share/extension/pldbgapi*.control
%if %llvm
 %{pginstdir}/lib/bitcode/plugin_debugger*.bc
 %{pginstdir}/lib/bitcode/plugin_debugger/*.bc
%endif


%changelog
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

