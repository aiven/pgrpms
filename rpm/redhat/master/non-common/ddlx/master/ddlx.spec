%global sname ddlx
%global pname pgddl

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	DDL eXtractor functions for PostgreSQL (ddlx)
Name:		%{sname}_%{pgmajorversion}
Version:	0.15
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/lacanoid/%{pname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/lacanoid/%{pname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This is an SQL-only extension for PostgreSQL that provides uniform functions
for generating SQL Data Definition Language (DDL) scripts for objects created
in a database. It contains a bunch of SQL functions to convert PostgreSQL
system catalogs to nicely formatted snippets of SQL DDL, such as CREATE TABLE.

%prep
%setup -q -n %{pname}-%{version}
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
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.md
%else
%license LICENSE.md
%endif
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*
%{pginstdir}/share/extension/%{sname}.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%changelog
* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 0.15.0.1
- Update to 0.15.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.14-2.1
- Rebuild for PostgreSQL 12

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 0.14-1
- Fix OS versions in Makefile, the distro name in the packages changed.

* Wed Aug 14 2019 Devrim Gündüz <devrim@gunduz.org> 0.14-1
- Initial packaging for PostgreSQL RPM Repository
