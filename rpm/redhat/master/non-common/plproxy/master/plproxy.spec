%global sname plproxy

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PL/Proxy is database partitioning system implemented as PL language.
Name:		%{sname}%{pgmajorversion}
Version:	2.9
Release:	1%{?dist}.1
License:	BSD
URL:		https://plproxy.github.io
Source0:	https://plproxy.github.io/downloads/files/%{version}/%{sname}-%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch

BuildRequires:	postgresql%{pgmajorversion}-devel flex >= 2.5.4
Requires:	postgresql%{pgmajorversion}
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
PL/Proxy is database partitioning system implemented as PL language.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md AUTHORS COPYRIGHT
%else
%license COPYRIGHT
%doc README.md AUTHORS COPYRIGHT
%endif
%{pginstdir}/lib/plproxy.so
%{pginstdir}/share/extension/plproxy--2.3.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--2.4.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--2.5.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--2.6.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--2.7.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--2.8.0--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--%{version}.0.sql
%{pginstdir}/share/extension/plproxy--unpackaged--%{version}.0.sql
%{pginstdir}/share/extension/plproxy.control

%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 9 2017 - Devrim Gündüz <devrim@gunduz.org> 2.8-1
- Update to 2.8

* Mon Jan 2 2017 - Devrim Gündüz <devrim@gunduz.org> 2.7-1
- Update to 2.7

* Fri Sep 11 2015 - Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6

* Tue Jan 15 2013 - Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Update download URL.

* Mon Feb 13 2012 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Tue Oct 12 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-2
- Apply 9.0 related changes to spec file.
- Get rid of ugly hacks in spec.

* Sat May 15 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Oct 28 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.9-1
- Update to 2.0.9

* Mon Feb 2 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.8-1
- Update to 2.0.8

* Tue Oct 7 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Sat Sep 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Sun Jun 15 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5
- Remove scanner.c and scanner.h, they are no longer needed.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Add pre-generated scanner.c and scanner.h as sources. Only very
recent versions of flex can compile plproxy.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial build 
