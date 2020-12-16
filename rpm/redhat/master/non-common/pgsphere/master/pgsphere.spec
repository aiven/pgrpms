%global sname pgsphere

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.1
Release:	5%{?dist}
License:	BSD
Source0:	https://download.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}/%{version}/%{sname}-%{version}.tar.gz
Source1:	%{sname}.control
Patch1:		%{sname}-int4.patch
Patch2:		%{sname}-makefile-extension.patch
URL:		http://pgfoundry.org/projects/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.1.1-5

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgSphere is a server side module for PostgreSQL. It contains methods for
working with spherical coordinates and objects. It also supports indexing of
spherical objects.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0
%patch2 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%endif
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 make install %{?_smp_mflags}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/contrib/COPYRIGHT.pg_sphere
%doc %{pginstdir}/doc/contrib/README.pg_sphere
%{pginstdir}/share/contrib/pg_sphere.sql
%{pginstdir}/lib/pg_sphere.so

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-5
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-4.1
- Rebuild against PostgreSQL 11.0

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-4
- Update for 9.5 doc layout.

* Thu Dec 12 2013 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-3
- Add a patch to fix build on Fedora 19
- Add extension support

* Mon Apr 15 2013 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-2
- Fix packaging issues, per report from Yukio Yamamoto:
  * Install pg_sphere.so under correct location. Actually
     trust make install there, do not manually install files.
  * Fix pg_sphere.sql, so that it can be loaded w/o errors to
    PostgreSQL 9.2.
- Update download URL.

* Wed Jan 5 2011 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per:
  http://pgfoundry.org/forum/forum.php?forum_id=1665

* Tue Jul 28 2009 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Wed Aug 20 2008 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Wed Apr 9 2008 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for Fedora
