%global sname pg_comparator

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.5
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/koordinates/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/koordinates/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires:	perl(Getopt::Long) perl(Time::HiRes) perl-Pod-Usage

Obsoletes:	%{sname}%{pgmajorversion} <= 2.2.5-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/share/contrib/

%post
# Create alternatives entries for binaries
%{_sbindir}/update-alternatives --install /usr/bin/%{sname} pgcomparator %{pginstdir}/bin/%{sname} %{pgmajorversion}0

%preun
# Drop alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --remove pgcomparator %{pginstdir}/bin/%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/contrib/README.%{sname}
%doc %{pginstdir}/doc/contrib/README.pgc_casts
%doc %{pginstdir}/doc/contrib/README.pgc_checksum
%doc %{pginstdir}/doc/contrib/README.xor_aggregate
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/%{sname}
%{pginstdir}/lib/pgc_casts.so
%{pginstdir}/lib/pgc_checksum.so
%{pginstdir}/share/contrib/*.sql
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/pgc_casts.index.bc
   %{pginstdir}/lib/bitcode/pgc_checksum.index.bc
   %{pginstdir}/lib/bitcode/pgc_casts/*.bc
   %{pginstdir}/lib/bitcode/pgc_checksum/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.2.5-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.2.5-2
- Add v11 support to spec file.

* Sun Jan 24 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5
- Unified spec file for all distros
- Use more macros
- Don't strip .so file
- Whitespace cleanup

* Thu Feb 13 2014 - Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sun Jun 30 2013 - Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Wed Nov 14 2012 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Sep 14 2012 - Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Use a better URL for tarball

* Fri Oct 8 2010 - Devrim Gündüz <devrim@gunduz.org> 1.6.2-1
- Refactor spec for 9.0 compatibility.

* Tue Apr 20 2010 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
