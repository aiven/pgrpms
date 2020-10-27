%global debug_package %{nil}
%global sname osm_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL foreign data wrapper OSM PBF
Name:		%{sname}_%{pgmajorversion}
Version:	4.0.0
Release:	2%{?dist}
License:	BSD
Source0:	https://api.pgxn.org/dist/osm_fdw/%{version}/osm_fdw-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
Patch1:		%{sname}-missinginclude.patch
URL:		https://github.com/vpikulik/postgres_osm_pbf_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel protobuf-c-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server, protobuf-c

Obsoletes:	%{sname}_%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with osm.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

strip %{buildroot}%{pginstdir}/lib/*.so

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%attr(755,root,root) %{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/%{sname}/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/osm_reader/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
