%global sname	pgexportdoc

Summary:	command line utility for exporting XML, JSON, BYTEA document from PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.1.4
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/okbob/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/okbob/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion} pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 0.1.3-2

%description
This PostgreSQL command line utility (extension) is used for exporting
XML, any text or binary documents from PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{pginstdir}/bin/%{sname}

%changelog
* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-3PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.4-1
- Update to 0.1.4

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.3-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.1.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 0.1.3-1
- Update to 0.1.3

* Wed Jul 5 2017 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
