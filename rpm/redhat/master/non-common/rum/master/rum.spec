%global sname	rum

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	RUM access method - inverted index with additional information in posting lists
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.7
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/postgrespro/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
The rum module provides access method to work with RUM index.
It is based on the GIN access methods code.

%package devel
Summary:	RUM access method development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package includes the development headers for the rum extension.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/include/server
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install}  -d %{buildroot}%{pginstdir}/doc/extension
%{__install}  -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
 %endif
%endif

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/rum*.h

%changelog
* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> 1.3.7-1
- Update to 1.3.7

* Wed Apr 1 2020 Devrim Gündüz <devrim@gunduz.org> 1.3.1-2
- Add missing BR and Requires
- Switch to pgdg-srpm-macros
- Fix rpmlint warning

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 1.2.1-2
- Rebuild against PostgreSQL 11.0

* Tue Jul 3 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
