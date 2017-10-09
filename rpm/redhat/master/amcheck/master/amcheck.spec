%global sname amcheck

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Functions for verifying PostgreSQL relation integrity
Name:		%{sname}%{pgmajorversion}
Version:	0.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/petergeoghegan/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/petergeoghegan/amcheck
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
The amcheck module provides functions that allow you to verify the
logical consistency of the structure of PostgreSQL indexes. If the
structure appears to be valid, no error is raised. Currently, only
B-Tree indexes are supported, although since in practice the
majority of PostgreSQL indexes are B-Tree indexes, amcheck is
likely to be effective as a general corruption smoke-test in
production PostgreSQL installations.

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
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
# Rename README file:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.md
%else
%license LICENSE.md
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Oct 9 2017 - Devrim Gündüz <devrim@gunduz.org> 0.3-1
- Initial packaging for PostgreSQL RPM repository.

