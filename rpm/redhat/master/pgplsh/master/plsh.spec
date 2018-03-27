%global sname plsh

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.20171014
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch1:		%{sname}-pg%{pgmajorversion}-makefile.patch
URL:		https://github.com/petere/plsh
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
PL/sh is a procedural language handler for PostgreSQL that
allows you to write stored procedures in a shell of your choice.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/%{sname}.so
%doc NEWS COPYING README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/share/extension/%{sname}--1--2.sql
%{pginstdir}/share/extension/%{sname}--2.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 1.20171014
- Update to 1.20171014

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20130823-2
- Cosmetic cleanup
- Use more macros for unified spec file

* Mon Mar 17 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.20130823-1
- Update to 1.20130823
- Update download URL

* Tue Nov 27 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.20121018-1
- Rewrite the spec file based on the new version, and update
  to 1.20121018

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for Fedora
