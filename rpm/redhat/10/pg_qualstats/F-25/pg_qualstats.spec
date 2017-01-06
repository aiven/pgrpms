%global pgmajorversion 10
%global pginstdir /usr/pgsql-10
%global sname pg_qualstats

Summary:	A PostgreSQL extension collecting statistics about predicates
Name:		%{sname}%{pgmajorversion}
Version:	1.0.2
Release:	1%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/pg_qualstats
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

#Avoid conflict with some other README file:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

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

%changelog
* Mon Oct 24 2016 - Devrim GUNDUZ <devrim@gunduz.org> - 1.0.2-1
- Update to 1.0.2

* Wed Sep 7 2016 - Devrim GUNDUZ <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1
- Add LICENSE file
- Update %%description

* Sun Mar 6 2016 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.9-1
- Update to 0.0.9

* Mon Jan 4 2016 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.7-1
- Update to 0.0.7
- Update for 9.5 doc layout.

* Thu Sep 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.6-1
- Update to 0.0.6

* Tue Mar 17 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
