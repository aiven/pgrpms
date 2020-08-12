%global sname tds_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	TDS Foreign Data Wrapper for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	2.0.1
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/tds-fdw/%{sname}/archive/v%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/tds-fdw/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel, freetds-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server, freetds

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This library contains a single PostgreSQL extension, a foreign data wrapper
called "tds_fdw". It can be used to communicate with Microsoft SQL
Server and Sybase databases.

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
%{__make}  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 ForeignSchemaImporting.md %{buildroot}%{pginstdir}/doc/extension/ForeignSchemaImporting-%{sname}.md
%{__install} -m 644 ForeignServerCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignServerCreation-%{sname}.md
%{__install} -m 644 ForeignTableCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignTableCreation-%{sname}.md
%{__install} -m 644 UserMappingCreation.md %{buildroot}%{pginstdir}/doc/extension/UserMappingCreation-%{sname}.md
%{__install} -m 644 Variables.md %{buildroot}%{pginstdir}/doc/extension/Variables-%{sname}.md
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}/%{pginstdir}/doc/extension/README.%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
* Wed Dec 4 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Sat Jan 19 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-alpha.3
- Update to 2.0.0-alpha.3 for testing repo only.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-alpha.2_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jul 31 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-alpha.2
- Update to 2.0.0-alpha.2 for testing repo only.

* Fri Oct 28 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.8-1
- Update to 1.0.8
- Change links to point to github.

* Thu Jan 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.7-1
- Update to 1.0.7
- Apply 9.5 doc layout.

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Fri Sep 25 2015  - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Initial packaging for PostgreSQL RPM Repository
