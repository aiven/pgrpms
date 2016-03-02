%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pgsphere

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}%{pgmajorversion}
Version:	1.1.1
Release:	4%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}/%{version}/%{sname}-%{version}.tar.gz
Source1:	pgsphere.control
Patch0:		pgsphere-pg92-languages.patch
Patch1:		pgsphere-int4.patch
Patch2:		pgsphere-makefile-extension.patch
URL:		http://pgfoundry.org/projects/pgsphere
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgSphere is a server side module for PostgreSQL. It contains methods for
working with spherical coordinates and objects. It also supports indexing of
spherical objects.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
make PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

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
* Mon Jan 4 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-4
- Update for 9.5 doc layout.

* Thu Dec 12 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-3
- Add a patch to fix build on Fedora 19
- Add extension support

* Mon Apr 15 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-2
- Fix packaging issues, per report from Yukio Yamamoto:
  * Install pg_sphere.so under correct location. Actually
     trust make install there, do not manually install files.
  * Fix pg_sphere.sql, so that it can be loaded w/o errors to
    PostgreSQL 9.2.
- Update download URL.

* Wed Jan 5 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per:
  http://pgfoundry.org/forum/forum.php?forum_id=1665

* Tue Jul 28 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Wed Aug 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Wed Apr 9 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for Fedora
