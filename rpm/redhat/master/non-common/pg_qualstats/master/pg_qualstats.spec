%global sname pg_qualstats

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	A PostgreSQL extension collecting statistics about predicates
Name:		%{sname}%{pgmajorversion}
Version:	2.0.1
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/powa-team/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/powa-team/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pg_qualstats is a PostgreSQL extension keeping statistics on
predicates found in WHERE statements and JOIN clauses.

This is useful if you want to be able to analyze what are
the most-often executed quals (predicates) on your database.
The powa project makes use of this to provide index
suggestions.

It also allows you to identify correlated columns, by
identifying which columns are most frequently queried
together.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file.
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%endif
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
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0
- Require pgdg-srpm-macros

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 - Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1
- Update to 1.0.9

* Wed Nov 21 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Update to 1.0.7

* Fri Nov 9 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.6-1
- Update to 1.0.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Fri Aug 10 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-2
- Ignore .bc files on PPC arch.

* Sun Aug 5 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1
- Update to 1.0.5
- Add PG 11 RPM support

* Sun Apr 15 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4
- Update URLs again.

* Sat Nov 18 2017 - Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3, per #2883.
- Update URLs

* Mon Oct 24 2016 - Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1
- Update to 1.0.2

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1
- Add LICENSE file
- Update %%description

* Sun Mar 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.9-1
- Update to 0.0.9

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.7-1
- Update to 0.0.7
- Update for 9.5 doc layout.

* Thu Sep 10 2015 - Devrim Gündüz <devrim@gunduz.org> 0.0.6-1
- Update to 0.0.6

* Tue Mar 17 2015 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
