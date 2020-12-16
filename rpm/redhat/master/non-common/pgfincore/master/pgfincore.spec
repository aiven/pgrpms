%global sname pgfincore

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PgFincore is a set of functions to manage blocks in memory
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/klando/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/klando/pgfincore
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.2-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PgFincore is a set of functions to manage blocks in memory.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}%{pginstdir}/share/pgfincore
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/pgfincore
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/pgfincore/README.md
%doc AUTHORS ChangeLog
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/pgfincore/%{sname}*.sql
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
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Sep 15 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1
- Update to 1.2.2
- Remove patch1, now in upstream

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1
- Add a patch (from git master) to fix build issues.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-2.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.2-2
- Fixes for Fedora 23 and PostgreSQL 9.5 doc layout.

* Tue Mar 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.2-1
- Update to 1.1.2
- Update project URL -- pgfoundry is dead.
- Update Source0 URL

* Mon Dec 19 2011 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per changes described in
  http://pgfoundry.org/forum/forum.php?forum_id=1859

* Fri Aug 12 2011 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Update to 1.0, (#68), per changes described in
  http://pgfoundry.org/frs/shownotes.php?release_id=1872

* Wed Nov 10 2010 - Devrim Gündüz <devrim@gunduz.org> 0.4.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
