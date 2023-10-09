%global sname	pgauditlogtofile

%if %{pgmajorversion} == 15
%global pgauditversion 17
%endif
%if %{pgmajorversion} == 14
%global pgauditversion 16
%endif
%if %{pgmajorversion} == 13
%global pgauditversion 15
%endif
%if %{pgmajorversion} == 12
%global pgauditversion 14
%endif
%if %{pgmajorversion} == 11
%global pgauditversion 13
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Audit Log To File Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.12
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server pgaudit%{pgauditversion}_%{pgmajorversion}

Obsoletes:	%{sname}-%{pgmajorversion} < 1.0-2

%description
The PostgreSQL Audit Log to File extension (pgauditlogtofile)
redirect PostgreSQL Audit extension (pgaudit) output to an
independent file.

The goal of the PostgreSQL Audit Log to file extension (pgauditlogtofile)
is to provide PostgreSQL users with capability to produce audit logs
often required to comply with government, financial, or ISO certifications.

An audit is an official inspection of an individual's or organization's
accounts, typically by an independent body. The information gathered by
the PostgreSQL Audit extension (pgaudit) is properly called an audit
trail or audit log. The term audit log is used in this documentation.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgauditlogtofile
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
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for pgauditlogtofile
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Oct 9 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.12-2PGDG
- Make conditionals also work on RHEL 8. Per
  https://redmine.postgresql.org/issues/7883

* Mon Jul 31 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.12-1PGDG
- Update to 1.5.12
- Add PGDG branding
- Update licence
- Fix rpmlint warnings
- Unify spec file for all versions

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.10-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue Dec 13 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.10-1
- Update to 1.5.10

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.6-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.6-2
- This package needs to require pgaudit17.

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.6-1
- Update to 1.5.6

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.5-1
- Update to 1.5.5

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Mon Oct 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2
- Remove pgxs patches, and export PATH instead.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Jun 06 2020 Francisco Miguel Biete Banon <fbiete@gmail.com> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
