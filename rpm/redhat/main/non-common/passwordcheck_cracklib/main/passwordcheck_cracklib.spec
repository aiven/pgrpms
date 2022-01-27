%global sname	passwordcheck_cracklib

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	1%{?dist}
Summary:	PostgreSQL passwordcheck extension, built with cracklib.
License:	BSD
URL:		https://github.com/devrimgunduz/%{sname}/
Source0:	https://github.com/devrimgunduz/%{sname}/archive/%{version}.tar.gz
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.2-3

BuildRequires:	cracklib-devel postgresql%{pgmajorversion}-devel pgdg-srpm-macros

%description
This is the regular PostgreSQL passwordcheck extension, built with cracklib.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
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
* Thu Jan 27 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Remove PGXS patches, and use PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.2-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Add v11 code to spec file

* Tue May 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial packaging
