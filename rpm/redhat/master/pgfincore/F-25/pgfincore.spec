%global pgmajorversion 10
%global pginstdir /usr/pgsql-10
%global sname pgfincore

Summary:	PgFincore is a set of functions to manage blocks in memory
Name:		%{sname}%{pgmajorversion}
Version:	1.1.2
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/klando/%{sname}/archive/%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		https://github.com/klando/pgfincore
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PgFincore is a set of functions to manage blocks in memory.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}%{pginstdir}/share/pgfincore
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/pgfincore
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/pgfincore/README.rst
%doc AUTHORS ChangeLog
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/pgfincore/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Mar 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.2-2
- Fixes for Fedora 23 and PostgreSQL 9.5 doc layout.

* Tue Mar 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.2-1
- Update to 1.1.2
- Update project URL -- pgfoundry is dead.
- Update Source0 URL

* Mon Dec 19 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per changes described in
  http://pgfoundry.org/forum/forum.php?forum_id=1859

* Fri Aug 12 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Update to 1.0, (#68), per changes described in
  http://pgfoundry.org/frs/shownotes.php?release_id=1872

* Wed Nov 10 2010 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
