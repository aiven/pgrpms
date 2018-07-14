%global sname pg_partman

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	A PostgreSQL extension to manage partitioned tables by time or ID
Name:		%{sname}%{pgmajorversion}
Version:	3.2.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/keithf4/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/keithf4/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pg_partman is a PostgreSQL extension to manage partitioned tables by time or ID.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%doc %{pginstdir}/doc/extension/%{sname}_howto.md
%{pginstdir}/lib/%{sname}_bgw.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/migration_to_partman.md
%attr(755, root, -) %{pginstdir}/bin/check_unique_constraint.py
%attr(755, root, -) %{pginstdir}/bin/reapply_constraints.py
%attr(755, root, -) %{pginstdir}/bin/reapply_foreign_keys.py
%attr(755, root, -) %{pginstdir}/bin/dump_partition.py
%attr(755, root, -) %{pginstdir}/bin/partition_data.py
%attr(755, root, -) %{pginstdir}/bin/reapply_indexes.py
%attr(755, root, -) %{pginstdir}/bin/undo_partition.py
%attr(755, root, -) %{pginstdir}/bin/vacuum_maintenance.py

%changelog
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
