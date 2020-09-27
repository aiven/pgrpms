%global sname pgbouncer_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	pgbouncer Foreign Data Wrapper
Name:		%{sname}%{pgmajorversion}
Version:	0.2
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/CrunchyData/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/CrunchyData/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	pgbouncer >= 1.10

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgbouncer_fdw provides a direct SQL interface to the pgbouncer SHOW commands.
It takes advantage of the dblink_fdw feature to provide a more typical,
table-like interface to the current status of your pgbouncer server(s).
This makes it easier to set up monitoring or other services that require
direct access to pgbouncer statistics.

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
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE.txt
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Mon Sep 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.2-1
- Initial packaging for PostgreSQL RPM Repository
