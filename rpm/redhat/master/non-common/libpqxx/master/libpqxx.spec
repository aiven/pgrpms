%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		libpqxx
Epoch:		1
Version:	6.4.5
Release:	1%{?dist}.1
Summary:	C++ client API for PostgreSQL

License:	BSD
URL:		https://github.com/jtv/%{name}
Source0:	https://github.com/jtv/%{name}/archive/%{version}.tar.gz

Patch0:		%{name}-python3.patch
BuildRequires:	postgresql%{pgmajorversion}-devel gcc-c++ cmake
BuildRequires:	pkgconfig doxygen xmlto

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
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
Requires:	postgresql%{pgmajorversion}-devel

%description devel
%{summary}.

%prep
%setup -q
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
%patch0 -p0
%endif

# fix spurious permissions
%{__chmod} -x COPYING

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
	PATH=%{atpath}/bin/:%{atpath}/sbin:$PATH ; export PATH
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
%doc README.md
%{_libdir}/%{name}*.so

%files devel
%defattr(-,root,root,-)
%doc README-UPGRADE
%{_includedir}/pqxx/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1:6.4.5-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 6.4.5-1
- Update to 6.4.5
- Add new patch for Python3 distros.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:5.0.1-2.1
- Rebuild against PostgreSQL 11.0

* Sun Oct 15 2017 Devrim Gündüz <devrim@gunduz.org> 5.0.1-2
- Fix linker issues during configure. Patch taken from Fedora.

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
