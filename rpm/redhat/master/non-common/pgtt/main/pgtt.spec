%global sname pgtt

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL Global Temporary Tables Extension
Name:		%{sname}_%{pgmajorversion}
Version:	2.4
Release:	1%{?dist}
License:	GPLv2
Source0:	https://github.com/darold/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/darold/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgtt is a PostgreSQL extension to create, manage and use Oracle-style Global
Temporary Tables and the others RDBMS.

The objective of this extension it to propose an extension to provide the
Global Temporary Table feature waiting for an in core implementation. The
main interest of this extension is to mimic the Oracle behavior with GTT when
you can not or don't want to rewrite the application code when migrating to
PostgreSQL. In all other case best is to rewrite the code to use standard
PostgreSQL temporary tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %make_install install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory with a better name:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}/%{pginstdir}/doc/extension/README.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license COPYING
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

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
* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4

* Fri Apr 2 2021 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3
- Export PATH, and remove pgxs patches.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Initial packaging for PostgreSQL RPM repository
