%global sname pguri

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	uri type for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.20151224
Release:	1%{?dist}.2
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch1:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/petere/pguri
BuildRequires:	postgresql%{pgmajorversion}-devel, uriparser-devel
Requires:	postgresql%{pgmajorversion}-server, uriparser

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This is an extension for PostgreSQL that provides a uri data type. Advantages
over using plain text for storing URIs include:

 * URI syntax checking
 * functions for extracting URI components
 * human-friendly sorting

The actual URI parsing is provided by the uriparser library, which supports
URI syntax as per RFC 3986.

Note that this might not be the right data type to use if you want to store
user-provided URI data, such as HTTP referrers, since they might contain
arbitrary junk.

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
%doc README.md
%{pginstdir}/lib/uri.so
%{pginstdir}/share/extension/uri-*.sql
%{pginstdir}/share/extension/uri.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/uri*.bc
   %{pginstdir}/lib/bitcode/uri/*.bc
  %endif
 %endif
%endif


%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20151224-1
- Update to 1.20151224

* Fri Apr 17 2015 - Devrim Gündüz <devrim@gunduz.org> 1.20150415-1
- Initial RPM packaging for PostgreSQL YUM Repository
