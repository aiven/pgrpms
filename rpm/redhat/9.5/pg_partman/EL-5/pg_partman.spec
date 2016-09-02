%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pg_partman

Summary:	A PostgreSQL extension to manage partitioned tables by time or ID
Name:		%{sname}%{pgmajorversion}
Version:	2.6.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/keithf4/%{sname}/archive/v%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		https://github.com/keithf4/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_partman is a PostgreSQL extension to manage partitioned tables by time or ID.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%doc %{pginstdir}/doc/extension/%{sname}_howto.md
%{pginstdir}/lib/%{sname}_bgw.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/migration.md
%attr(755, root, -) %{pginstdir}/bin/check_unique_constraint.py
%attr(755, root, -) %{pginstdir}/bin/reapply_constraints.py
%attr(755, root, -) %{pginstdir}/bin/reapply_foreign_keys.py
%attr(755, root, -) %{pginstdir}/bin/dump_partition.py
%attr(755, root, -) %{pginstdir}/bin/partition_data.py
%attr(755, root, -) %{pginstdir}/bin/reapply_indexes.py
%attr(755, root, -) %{pginstdir}/bin/undo_partition.py
%attr(755, root, -) %{pginstdir}/bin/vacuum_maintenance.py

%changelog
* Wed Aug 31 2016 - Devrim GUNDUZ <devrim@gunduz.org> 2.6.0-1
- Update to 2.6.0

* Mon Jul 4 2016 - Devrim GUNDUZ <devrim@gunduz.org> 2.4.1-1
- Update to 2.4.1

* Thu Mar 3 2016 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Mon Jan 4 2016 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Fri Sep 25 2015 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Tue Jun 16 2015 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Wed Feb 25 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0
- Remove executable bit from docs

* Wed Jun 18 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Apr 29 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.7.0-1
- Update to 1.7.0

* Thu Mar 6 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Feb 15 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Jan 15 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Thu Oct 31 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.4.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
