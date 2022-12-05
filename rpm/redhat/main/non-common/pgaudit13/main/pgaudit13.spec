%global sname	pgaudit

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Audit Extension
Name:		%{sname}13_%{pgmajorversion}
Version:	1.3.4
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/%{version}.tar.gz
URL:		https://www.pgaudit.org
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Audit extension (pgaudit) provides detailed session
and/or object audit logging via the standard PostgreSQL logging
facility.

The goal of the PostgreSQL Audit extension (pgaudit) is to provide
PostgreSQL users with capability to produce audit logs often required to
comply with government, financial, or ISO certifications.

An audit is an official inspection of an individual's or organization's
accounts, typically by an independent body. The information gathered by
the PostgreSQL Audit extension (pgaudit) is properly called an audit
trail or audit log. The term audit log is used in this documentation.

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/pgaudit*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Mar 4 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-2
- Remove pgxs patches, and export PATH instead.

* Tue Oct 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2

* Sun May 10 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2
- Fix pgdg-srpm-macros dependency. Per John.

* Mon Mar 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Mon Oct 22 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.1
- Initial RPM packaging for PostgreSQL RPM Repository
