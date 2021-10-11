%global sname	pgauditlogtofile

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL Audit Log To File Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.4
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server pgaudit15_%{pgmajorversion}

Obsoletes:	%{sname}-%{pgmajorversion} < 1.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

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

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

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
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
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
