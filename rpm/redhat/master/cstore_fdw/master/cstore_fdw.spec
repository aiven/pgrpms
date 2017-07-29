%global sname cstore_fdw

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Columnar store extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.6.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://citusdata.github.io/cstore_fdw/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	protobuf-c-devel

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
cstore_fdw is column-oriented store available for PostgreSQL. Using it will
let you:
    Leverage typical analytics benefits of columnar stores
    Deploy on stock PostgreSQL or scale-out PostgreSQL (CitusDB)

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

%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-cstore_fdw.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sun Jul 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0
- Add LICENSE among installed files.

* Thu Jun 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4
- Parallel build seems to be broken, so disable it for now.

* Mon Sep 07 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Aug 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
