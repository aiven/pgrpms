%global sname	plr
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Procedural language interface between PostgreSQL and R
Name:		%{sname}%{pgmajorversion}
Version:	8.3.0.17
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/postgres-%{sname}/%{sname}/archive/REL8_3_0_17.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/postgres-%{sname}/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel R-devel
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
Procedural Language Handler for the "R software environment for
statistical computing and graphics".

%prep
%setup -q -n %{sname}-REL8_3_0_17
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 DESTDIR=%{buildroot}/ install

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README.%{sname}
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Wed Sep 28 2016 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-17-1
- Update to 8.3.0.17

* Mon Feb 23 2015 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-16-1
- Update to 8.3.0.16

* Sat Dec 28 2013 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-15-1
- Update to 8.3.0.15

* Mon Mar 25 2013 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-14-1
- Update to 8.3.0.14
- Remove patch that I added in 8.3.0.13-2, now it is upstream.

* Tue Oct 09 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.3.0.13-2
- Add a patch for plr extension to be installed on PostgreSQL 9.2. Per report
  from Jose Pedro Oliveira

* Tue Sep 11 2012 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-13-1
- Update to 8.3.0.13

* Fri Oct 8 2010 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-11-1
- Initial packaging for 9.0, which also suits new PostgreSQL RPM layout.
