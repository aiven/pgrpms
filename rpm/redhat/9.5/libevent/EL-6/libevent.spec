%if 0%{?fedora} && 0%{?fedora} >= 20
%global develdocdir %{_docdir}/%{name}-devel
%else
%global develdocdir %{_docdir}/%{name}-devel-%{version}
%endif

Name:		libevent
Version:	2.0.22
Release:	1%{?dist}
Summary:	Abstract asynchronous event notification library

Group:		System Environment/Libraries
License:	BSD
URL:		http://sourceforge.net/projects/levent
Source0:	http://downloads.sourceforge.net/levent/%{name}-%{version}-stable.tar.gz

BuildRequires:	doxygen openssl-devel

Patch0:		libevent-2.0.10-stable-configure.patch
# Disable network tests
Patch1:		libevent-nonettests.patch

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and libraries for developing
with %{name}.

%package doc
Summary:	Development documentation for %{name}
Group:		Documentation
BuildArch:	noarch

%description doc
This package contains the development documentation for %{name}.

%prep
%setup -q -n libevent-%{version}-stable

# 477685 -  libevent-devel multilib conflict
%patch0 -p0
%patch1 -p1 -b .nonettests

%build
%configure \
    --disable-dependency-tracking --disable-static
make %{?_smp_mflags} all

# Create the docs
make doxygen

%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{_libdir}/*.la

%{__mkdir} -p %{buildroot}/%{develdocdir}/html
(cd doxygen/html; \
	install -p -m 644 *.* %{buildroot}/%{develdocdir}/html)

%{__mkdir}  -p %{buildroot}/%{develdocdir}/sample
(cd sample; \
	install -p -m 644 *.c Makefile* %{buildroot}/%{develdocdir}/sample)

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog LICENSE README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*
%{_libdir}/libevent_openssl-*.so.*
%{_libdir}/libevent_pthreads-*.so.*

%files devel
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%dir %{_includedir}/event2
%{_includedir}/event2/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*

%files doc
%{develdocdir}/

%changelog
* Tue Nov 24 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.0.22-1
- Update to 2.0.22
- Some fixes from Fedora packaging:
 * Fix -doc package for F20 UnversionedDocDirs (#993956)
 * Add missing directory /usr/include/event2
 * Fix directory ownership in -doc package
 * Correct summary and description of -devel and -doc packages
 * Set -doc package Group tag to "Documentation"
 * Add %%?_isa to -devel package base dependency
 * Remove %%defattr

* Fri Jul 27 2012 Devrim GUNDUZ <devrim@gunduz.org> 2.0.19-1
- Update to 2.0.19

* Tue Aug 09 2011 Devrim GUNDUZ <devrim@gunduz.org> 2.0.12-1
- Update to 2.0.12

* Thu Nov 11 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.4.13-2
- Update to 1.4.13
- Use bigger release number, so that repos will pick up this one.

* Tue Jan 13 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.4.9-1
- Initial build for PostgreSQL RPM Repository, based on Fedora spec.

