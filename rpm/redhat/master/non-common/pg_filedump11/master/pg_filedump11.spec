%global sname pg_filedump
%global sversion REL_11_0

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	11.0
Release:	2%{?dist}
URL:		https://github.com/df7cb/%{sname}
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Source0:	https://github.com/df7cb/%{sname}/archive/%{sversion}.tar.gz
Patch1:		pg_filedump-pg%{pgmajorversion}-makefile-pgxs.patch

Obsoletes:	%{sname}%{pgmajorversion} < 11.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}
%patch1 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 11.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 11.0-1
- Initial packaging for PostgreSQL RPM Repository
