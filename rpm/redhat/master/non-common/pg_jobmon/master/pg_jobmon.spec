%global sname pg_jobmon

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Job logging and monitoring extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	2%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/pg_jobmon/%{version}/pg_jobmon-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/omniti-labs/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
BuildArch:	noarch

Obsoletes:	%{sname}%{pgmajorversion} <= 1.4.0-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pg_jobmon is a job logging and monitoring extension for PostgreSQL.

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
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.4.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Oct 25 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-2.1
- Rebuild for PostgreSQL 12

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-2
- Add -contrib dependency, required for dblink extension.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu Jul 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3
- Update URLs

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2
- Use the new directory for docs.

* Tue Apr 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Thu Oct 31 2013 - Devrim Gündüz <devrim@gunduz.org> 1.1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
