%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pgmemcache

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}-%{pgmajorversion}
Version:	2.3.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/ohmu/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		https://github.com/Ohmu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel, libmemcached-devel, cyrus-sasl-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

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

%changelog
* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Use more macros in spec file

* Wed Nov 20 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2
- Fix various issues in init script

* Sat Jul 3 2010 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.4-1
- Initial packaging for PostgreSQL RPM Repository
