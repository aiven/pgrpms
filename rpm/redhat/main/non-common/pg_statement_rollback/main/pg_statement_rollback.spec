%global sname pg_statement_rollback

Summary:	Server side rollback at statement level for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/lzlabs/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/lzlabs/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_statement_rollback is a PostgreSQL extension to add server side
transaction with rollback at statement level like in Oracle or DB2.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
# Install documentation with a better name:
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/contrib/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%doc %{pginstdir}/doc/extension/README-%{sname}.md
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
* Mon Oct 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Remove pgxs patches, and export PATH instead.

* Thu Nov 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
