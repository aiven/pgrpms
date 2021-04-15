%global sname pg_stat_monitor

%global monitormajver 0
%global monitormidver 9
%global monitorminver 1

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL Query Performance Monitoring Tool
Name:		%{sname}_%{pgmajorversion}
Version:	0.9.1
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/percona/%{sname}
Source0:	https://github.com/percona/%{sname}/archive/REL%{monitormajver}_%{monitormidver}_%{monitorminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.1.3-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
The pg_stat_monitor is a PostgreSQL Query Performance Monitoring tool, based
on PostgreSQL's contrib module pg_stat_statements. PostgreSQL’s
pg_stat_statements provides the basic statistics, which is sometimes not
enough. The major shortcoming in pg_stat_statements is that it accumulates
all the queries and their statistics and does not provide aggregated
statistics nor histogram information. In this case, a user needs to calculate
the aggregate which is quite expensive.

pg_stat_monitor is developed on the basis of pg_stat_statements as its more
advanced replacement. It provides all the features of pg_stat_statements
plus its own feature set.

%prep
%setup -q -n %{sname}-REL%{monitormajver}_%{monitormidver}_%{monitorminver}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc docs/
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
 %endif
%endif

%changelog
* Thu Apr 15 2021 - Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1

* Thu Jan 28 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-2
- Fix distro part in RPM names.

* Thu Jan 21 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
