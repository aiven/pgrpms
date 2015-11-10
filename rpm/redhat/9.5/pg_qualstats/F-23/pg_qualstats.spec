%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pg_qualstats

Summary:	A PostgreSQL extension collecting statistics about predicates
Name:		%{sname}%{pgmajorversion}
Version:	0.0.6
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
This software is EXPERIMENTAL and therefore NOT production ready. Use at your
own risk.

pg_qualstats is a PostgreSQL extension keeping statistics on predicates found
in WHERE statements and JOIN clauses.

Most of the code is a blatant rip-off of pg_stat_statements.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
rm -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Sep 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.6-1
- Update to 0.0.6

* Tue Mar 17 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
