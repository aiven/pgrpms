%global sname wal2json
%global wal2json_rel 2_5

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	JSON output plugin for changeset extraction
Name:		%{sname}_%{pgmajorversion}
Version:	2.5
Release:	3%{?dist}.1
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{wal2json_rel}.tar.gz
URL:		https://github.com/eulerto/wal2json
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.3-3

%description
wal2json is an output plugin for logical decoding. It means that the
plugin have access to tuples produced by INSERT and UPDATE. Also,
UPDATE/DELETE old row versions can be accessed depending on the
configured replica identity. Changes can be consumed using the streaming
protocol (logical replication slots) or by a special SQL API.

The wal2json output plugin produces a JSON object per transaction. All
of the new/old tuples are available in the JSON object. Also, there are
options to include properties such as transaction timestamp,
schema-qualified, data types, and transaction ids.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for wal2json
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
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for wal2json
%endif


%prep
%setup -q -n %{sname}-%{sname}_%{wal2json_rel}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}/%{pginstdir}/doc/extension/
%{__mv} README.md  %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
  %{pginstdir}/lib/bitcode/%{sname}*.bc
  %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.5-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 14 2022 - John Harvey <john.harvey@crunchydata.com> 2.5-2
- Remove duplicated macros

* Tue Oct 11 2022 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5
- Split LLVM stuff into their own subpackage.

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3-4
- Remove PGXS patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Aug 11 2020 - John Harvey <john.harvey@crunchydata.com> 2.3-2
- Fix source pathing

* Tue Aug 11 2020 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Mon Apr 27 2020 - John Harvey <john.harvey@crunchydata.com> 2.2-2
- Fix source pathing

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Mon Jan 6 2020 - John Harvey <john.harvey@crunchydata.com> 2.0-2
- fix source pathing

* Sun Jan 5 2020 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Jan 2 2020 - John Harvey <john.harvey@crunchydata.com> 1.0-4
- Update license type

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.0-3
- Rebuild against PostgreSQL 11.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.2.1
- Rebuild against PostgreSQL 11.0

* Sat Aug 11 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Ignore .bc files on PPC arch.

* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for yum.postgresql.org
