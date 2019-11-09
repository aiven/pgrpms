%global sname postgresql_anonymizer

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Anonymization & Data Masking for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.5.0
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://gitlab.com/daamien/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib ddlx_%{pgmajorversion}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

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
%{pginstdir}/lib/anon.so
%{pginstdir}/share/extension/anon/*
%{pginstdir}/share/extension/anon.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/anon*.bc
   %{pginstdir}/lib/bitcode/anon/*.bc
  %endif
 %endif
%endif

%changelog
* Sat Nov 9 2019 Devrim Gündüz <devrim@gunduz.org> 0.5.0-1
- Update to 0.5.0

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-2
- Require -contrib subpackage for tsm_system_rows extension. Per
  Damien: https://redmine.postgresql.org/issues/4861

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-1
- Update to 0.4.1

* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1.1
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Wed Aug 14 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0
- Add ddlx dependency

* Tue Nov 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.2.1-1
- Initial packaging for PostgreSQL RPM Repository
