%global sname pgreplay
%global vname PGREPLAY_1_3_0

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL log file re-player
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/laurenz/pgreplay/archive/%{vname}.tar.gz
URL:		https://github.com/laurenz/pgreplay
Requires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

Obsoletes:	%{sname}%{pgmajorversion} < 1.3.0-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgreplay reads a PostgreSQL log file (not a WAL file), extracts the SQL
statements and executes them in the same order and relative time against
a PostgreSQL database cluster.

If the execution of statements gets behind schedule, warning messages
are issued that indicate that the server cannot handle the load in a
timely fashion. The idea is to replay a real-world database workload as
exactly as possible.

pgreplay is useful for performance tests, particularly in the following
situations:

* You want to compare the performance of your PostgreSQL application
on different hardware or different operating systems.
* You want to upgrade your database and want to make sure that the new
database version does not suffer from performance regressions that
affect you.

%prep
%setup -q -n %{sname}-%{vname}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

%configure --with-postgres=%{pginstdir}/bin
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Rename files for multiple version installation
%{__mv} %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{sname}%{pgmajorversion}
%{__mv} %{buildroot}%{_mandir}/man1/%{sname}.1 %{buildroot}%{_mandir}/man1/%{sname}%{pgmajorversion}.1.gz

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc pgreplay.html README CHANGELOG
%{_bindir}/%{sname}%{pgmajorversion}
%{_mandir}/man1/%{sname}*

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Mon Sep 10 2012 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial RPM packaging for Fedora

