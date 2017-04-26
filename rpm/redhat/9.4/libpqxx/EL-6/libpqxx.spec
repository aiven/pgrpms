%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		libpqxx
Epoch:		1
Version:	5.0.1
Release:	1%{?dist}
Summary:	C++ client API for PostgreSQL

Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/jtv/%{name}
Source0:	https://github.com/jtv/%{name}/archive/5.0.1.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch3:		%{name}-2.6.8-multilib.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	pkgconfig

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%package devel
Summary:	Development tools for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
Requires:	postgresql%{pgmajorversion}-devel

%description devel
%{summary}.

%prep
%setup -q

# fix spurious permissions
%{__chmod} -x COPYING

%patch3 -p1 -b .multilib

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
export PG_CONFIG=%{pginstdir}/bin/pg_config
%configure --enable-shared --disable-static

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%{__rm} -f %{buildroot}%{_libdir}/lib*.la

%check
# not enabled, by default, takes awhile.
%{?_with_check:make check}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md ChangeLog
%{_libdir}/%{name}-5.0.so

%files devel
%defattr(-,root,root,-)
%doc README-UPGRADE
%{_bindir}/pqxx-config
%{_includedir}/pqxx/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Apr 26 2017 Devrim Gündüz <devrim@gunduz.org> 5.0.1-1
- Update to 5.0.1
- Update URLs
- Add support for Power RPMs.
- Fix rpmlint warnings.

* Mon Sep 16 2013 Devrim Gündüz <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1, per changes described at:
  http://pqxx.org/development/libpqxx/browser/tags/4.0.1/NEWS

* Fri Apr 6 2012 Devrim Gündüz <devrim@gunduz.org> 4.0-1
- Update to 4.0

* Fri Aug 12 2011 Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1
- Sync with Fedora rawhide spec
- Trim changelog
