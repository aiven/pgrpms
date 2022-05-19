%global sname pg_partman

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if 0%{?fedora} > 32 || 0%{?rhel} >= 7
%{!?with_python3:%global with_python3 1}
%endif

Summary:	A PostgreSQL extension to manage partitioned tables by time or ID
Name:		%{sname}_%{pgmajorversion}
Version:	4.6.2
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgpartman/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/pgpartman/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 7
Requires:	python3-psycopg2
%endif

Obsoletes:	%{sname}%{pgmajorversion} < 4.4.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pg_partman is a PostgreSQL extension to manage partitioned tables by time or ID.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

# Change Python path in the scripts:
%if 0%{?with_python3}
find . -iname "*.py" -exec sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/python3/g" {} \;
%else
find . -iname "*.py" -exec sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/python2/g" {} \;
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%doc %{pginstdir}/doc/extension/%{sname}_howto_native.md
%doc %{pginstdir}/doc/extension/%{sname}_howto_triggerbased.md
%{pginstdir}/lib/%{sname}_bgw.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/migration_to_partman.md
%{pginstdir}/doc/extension/migrate_to_native.md
%attr(755, root, -) %{pginstdir}/bin/check_unique_constraint.py
%attr(755, root, -) %{pginstdir}/bin/dump_partition.py
%attr(755, root, -) %{pginstdir}/bin/reapply_indexes.py
%attr(755, root, -) %{pginstdir}/bin/vacuum_maintenance.py
# Some python scripts were moved to procedures in PG11:
%if %{pgmajorversion} >= 90 || %{pgmajorversion} == 10
%attr(755, root, -) %{pginstdir}/bin/partition_data.py
%attr(755, root, -) %{pginstdir}/bin/reapply_constraints.py
%attr(755, root, -) %{pginstdir}/bin/reapply_foreign_keys.py
%attr(755, root, -) %{pginstdir}/bin/undo_partition.py
%endif
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/src/pg_partman_bgw.index.bc
   %{pginstdir}/lib/bitcode/src/pg_partman_bgw/src/pg_partman_bgw.bc
  %endif
 %endif
%endif

%changelog
* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.6.2-1
- Update to 4.6.2

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 4.6.1-1
- Update to 4.6.1

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1
- Update to 4.6.0

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-2
- Remove pgxs patches, and export PATH instead.

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1
- Update to 4.5.1

* Wed Apr 14 2021 John Harvey <john.harvey@crunchydata.com> - 4.5.0-1
- Update to 4.5.0

* Thu Jan 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-1
- Update to 4.4.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.4.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1
- Update to 4.4.0

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Update to 4.3.0
- Switch to PY3 on RHEL 7

* Fri Nov 1 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-2
- Depend on python3-psycopg2 on RHEL >= 7, and Fedora. Use python-psycopg2
  on RHEL 6.

* Fri Oct 25 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1
- Update to 4.2.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Aug 22 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1
- Update to 4.2.0

* Thu Apr 25 2019 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0
- Fix Python paths.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 15 2018 - John K. Harvey <john.harvey@crunchydata.com> 4.0.0-1
- Update to 4.0.0

* Fri Jul 27 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1, per #3519

* Sat Jul 14 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2.0-1
- Update to 3.2.0

* Tue Apr 24 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.3-1
- Update to 3.1.3

* Sun Feb 4 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.2-1
- Update to 3.1.2

* Fri Jan 12 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.1-1
- Update to 3.1.1

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-1
- Update to 3.1.0

* Fri Jun 2 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Sat Dec 3 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2

* Mon Oct 24 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1

* Wed Aug 31 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.0-1
- Update to 2.6.0

* Mon Jul 4 2016 - Devrim Gündüz <devrim@gunduz.org> 2.4.1-1
- Update to 2.4.1

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Fri Sep 25 2015 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Tue Jun 16 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Wed Feb 25 2015 - Devrim Gündüz <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0
- Remove executable bit from docs

* Wed Jun 18 2014 - Devrim Gündüz <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Apr 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.7.0-1
- Update to 1.7.0

* Thu Mar 6 2014 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Feb 15 2014 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Jan 15 2014 - Devrim Gündüz <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Thu Oct 31 2013 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
