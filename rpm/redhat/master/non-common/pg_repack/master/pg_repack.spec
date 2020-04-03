%global debug_package %{nil}

%global sname	pg_repack

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Reorganize tables in PostgreSQL databases without any locks
Name:		%{sname}%{pgmajorversion}
Version:	1.4.5
Release:	1%{?dist}
License:	BSD
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		pg_repack-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://pgxn.org/dist/pg_repack/

BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pg_repack can re-organize tables on a postgres database without any locks so that
you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

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
USE_PGXS=1 make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 make DESTDIR=%{buildroot} install

%files
%defattr(644,root,root)
%doc COPYRIGHT doc/pg_repack.rst
%attr (755,root,root) %{pginstdir}/bin/pg_repack
%attr (755,root,root) %{pginstdir}/lib/pg_repack.so
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
  %endif
 %endif
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.5-1
- Update to 1.4.5

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.4-1
- Update to 1.4.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu May 24 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Update to 1.4.3

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2, per #2791

* Wed Aug 16 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1, per #2364

* Fri Apr 28 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0, per #2364

* Wed Jun 1 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #1272

* Fri Feb 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3

* Wed Sep 9 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Tue May 20 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Fri Mar 23 2012 - Devrim Gunduz <devrim@gunduz.org> 1.1.7-1
- Initial packaging for PostgreSQL RPM Repository, based on the
  NTT spec, simplified and modified for PostgreSQL RPM compatibility.
- Cleaned up various rpmlint errors and warnings.
