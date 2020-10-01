%global sname	sqlite_fdw

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

Summary:	SQLite Foreign Data Wrapper for PostgreSQL

Name:		%{sname}%{pgmajorversion}
Version:	1.3.0
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	https://github.com/pgspider/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	postgresql%{pgmajorversion}-server sqlite-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} >= 27
Requires:	sqlite-libs
%endif
%if 0%{?rhel} <= 7
Requires:	sqlite
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This PostgreSQL extension is a Foreign Data Wrapper for SQLite.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md
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
* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Wed Oct 31 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM repositories
