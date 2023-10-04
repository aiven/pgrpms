%global sname pglogical
%global tag 2_4_4

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Logical Replication extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.4.4
Release:	1PGDG%{dist}
License:	PostgreSQL
URL:		https://github.com/2ndQuadrant/%{sname}
Source0:	https://github.com/2ndQuadrant/%{sname}/archive/REL%{tag}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}_%{pgmajorversion} < 2.3.3-2

%description
pglogical is a logical replication system implemented entirely as a PostgreSQL
extension. Fully integrated, it requires no triggers or external programs.
This alternative to physical replication is a highly efficient method of
replicating data using a publish/subscribe model for selective replication.

he pglogical 2 extension provides logical streaming replication for
PostgreSQL, using a publish/subscribe model.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pglogical
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
This packages provides JIT support for pglogical
%endif

%prep
%setup -q -n %{sname}-REL%{tag}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%license COPYRIGHT
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/bin/%{sname}_create_subscriber
%{pginstdir}/lib/%{sname}_output.so
%{pginstdir}/share/extension/%{sname}_origin--1.0.0.sql
%{pginstdir}/share/extension/%{sname}_origin.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}_output/*.bc
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/compat%{pgmajorversion}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc*
%endif

%changelog
* Wed Oct 4 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.4.4-1
- Update to 2.4.4

* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 30 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.4.3-1
- Update to 2.4.3

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 21 2022 - John Harvey <john.harvey@crunchydata.com> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-2
- Update SLES 15 dependencies for SP4.

* Wed Mar 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2
- Rebuild against LLVM 11 on SLES 15.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Tue Aug 17 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
* Tue Aug 17 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
- Split llvmjit bits into a separate package

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 2.3.4-1
- Update to 2.3.4

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.3-1
- Update to 2.3.3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun May 3 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Initial RPM packaging for PostgreSQL RPM Repository,
