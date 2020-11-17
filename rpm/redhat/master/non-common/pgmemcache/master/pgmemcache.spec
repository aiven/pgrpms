%global sname pgmemcache

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	4%{?dist}
License:	BSD
Source0:	https://github.com/ohmu/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/Ohmu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libmemcached-devel
BuildRequires:	pgdg-srpm-macros cyrus-sasl-devel
Requires:	postgresql%{pgmajorversion}-server libmemcached

Obsoletes:	%{sname}-%{pgmajorversion} < 2.3.0-4

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

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

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/lib/pgmemcache.so
%{pginstdir}/share/extension/pgmemcache--*.sql
%{pginstdir}/share/extension/pgmemcache.control
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
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-4
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3.1
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-3
- Add v11+ support

* Mon Jul 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Add libmemcached dependency, per Fahar Abbas (EDB QA)

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Use more macros in spec file

* Wed Nov 20 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2
- Fix various issues in init script

* Sat Jul 3 2010 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.4-1
- Initial packaging for PostgreSQL RPM Repository
