%global debug_package %{nil}

%global sname	plv8
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	1%{?dist}.1
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/%{sname}/%{sname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, v8-devel >= 3.14.5, gcc-c++
BuildRequires:	platform-devel
%if 0%{?fedora} > 24
BuildRequires:	ncurses-compat-libs
%endif
%if 0%{?rhel} && 0%{?rhel} >= 7
BuildRequires:	ncurses-libs
%endif
Requires:	postgresql%{pgmajorversion}, v8 >= 3.14.5
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
plv8 is a shared library that provides a PostgreSQL procedural language
powered by V8 JavaScript Engine. With this program you can write in JavaScript
your function that is callable from SQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} static %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot} %{?_smp_mflags}
%{__rm} -f  %{buildroot}%{_datadir}/*.sql

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md doc/%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/plcoffee--%{version}.sql
%{pginstdir}/share/extension/plcoffee.control
%{pginstdir}/share/extension/plls--%{version}.sql
%{pginstdir}/share/extension/plls.control
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Sun Oct 22 2017 Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Sun May 28 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Sun Feb 19 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Sat Dec 3 2016 Devrim Gündüz <devrim@gunduz.org> 1.5.4-1
- Update to 1.5.4

* Thu Mar 3 2016 Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Jul 23 2015 Devrim Gündüz <devrim@gunduz.org> 1.4.4-1
- Update to 1.4.4
- Update URL

* Wed Jul 9 2014 Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Dec 12 2013 Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Initial spec file, per RH #1036130, after doing modifications
  to suit community RPM layout. Original work is by David
  Wheeler and Mikko Tiihonen
