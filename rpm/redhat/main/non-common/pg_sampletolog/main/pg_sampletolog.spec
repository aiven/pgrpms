%global sname pg_sampletolog

Summary:	Postgres extension to sample statements or transactions to logs
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	4%{?dist}
License:	BSD
Source0:	https://github.com/anayrat/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/anayrat/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <= 2.0.0-2

%description
pg_sampletolog is a PostgreSQL extension which allows to sample
statements and/or transactions to logs. It add in PostgreSQL (from 9.4
to 11) same kind of statement sampling added in PostgreSQL 12 (currently
not released).

pg_sampletolog allows to:

 -  Log a sample of statements
 -  Log a sample of transactions
 -  Log before or after execution (in order to be compatible with
    pgreplay)
 -  Log all DDL or MOD statements, same as log_statement
 -  Log statement's queryid if pg_stat_statements is installed

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%license LICENSE
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
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-4
- Remove pgxs patches, and export PATH instead.

* Sun Dec 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-3
- Fix upgrade path breakage.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed Apr 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM Repository
