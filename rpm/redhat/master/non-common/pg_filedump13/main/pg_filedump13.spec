%global sname pg_filedump
%global sversion REL_13_0

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	13.0
Release:	1%{?dist}
URL:		https://github.com/df7cb/%{sname}
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Source0:	https://github.com/df7cb/pg_filedump/archive/%{sversion}.tar.gz
Patch1:		pg_filedump-pg%{pgmajorversion}-makefile-pgxs.patch

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
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
* Wed Oct 28 2020 Devrim Gündüz <devrim@gunduz.org> - 13.0-1
- Initial packaging for PostgreSQL RPM Repository
