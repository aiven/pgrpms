%global sname	plr

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Procedural language interface between PostgreSQL and R
Name:		%{sname}_%{pgmajorversion}
Version:	8.4.3
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/postgres-%{sname}/%{sname}/archive/REL8_4_3.tar.gz
URL:		https://github.com/postgres-%{sname}/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel R-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 8.4.1-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Procedural Language Handler for the "R software environment for
statistical computing and graphics".

%prep
%setup -q -n %{sname}-REL8_4_3

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot}/ install

# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc changelog.md compilingplr.md userguide.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
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
* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 8.4.3-1
- Update to 8.4.3

* Sat May 29 2021 Devrim Gündüz <devrim@gunduz.org> - 8.4.2-1
- Update to 8.4.2, per changes described at:
  https://github.com/postgres-plr/plr/blob/REL8_4_2/changelog.md
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 8.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Sep 14 2020 Devrim Gündüz <devrim@gunduz.org> - 8.4.1-1
- Update to 8.4.1

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-2.1
- Rebuild for PostgreSQL 12

* Fri Jul 12 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-2
- Rebuilt, per a potential packaging issue reported by Dave Cramer.

* Tue Jun 4 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-1
- Update to 8.4
- Rename README file, so that it is consistent with many other packages.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Oct 1 2018 - John K. Harvey <john.harvey@crunchydata.com> 8.3.0-18-1
- Update to 8.3.0.18
- PG11 LLVM support

* Wed Sep 28 2016 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-17-1
- Update to 8.3.0.17

* Mon Feb 23 2015 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-16-1
- Update to 8.3.0.16

* Sat Dec 28 2013 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-15-1
- Update to 8.3.0.15

* Mon Mar 25 2013 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-14-1
- Update to 8.3.0.14
- Remove patch that I added in 8.3.0.13-2, now it is upstream.

* Tue Oct 09 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.3.0.13-2
- Add a patch for plr extension to be installed on PostgreSQL 9.2. Per report
  from Jose Pedro Oliveira

* Tue Sep 11 2012 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-13-1
- Update to 8.3.0.13

* Fri Oct 8 2010 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-11-1
- Initial packaging for 9.0, which also suits new PostgreSQL RPM layout.
