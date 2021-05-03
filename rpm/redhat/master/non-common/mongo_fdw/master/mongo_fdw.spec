%global sname mongo_fdw
%global relver 5_2_8

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	5.2.8
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{relver}.tar.gz
Source1:	%{sname}-config.h
%ifarch ppc64 ppc64le
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs-ppc64le.patch
%else
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs-x86.patch
%endif
%ifarch ppc64 ppc64le
Patch1:		mongo_fdw-autogen-ppc64le.patch
%endif
URL:		https://github.com/EnterpriseDB/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel wget pgdg-srpm-macros
BuildRequires:	mongo-c-driver-devel snappy snappy-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 5.2.7-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
MongoDB.

%prep
%setup -q -n %{sname}-REL-%{relver}
%patch0 -p0
%ifarch ppc64 ppc64le
%patch1 -p0
%endif
%{__cp} %{SOURCE1} ./config.h

%build
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -fPIC -I%{atpath}/include"; export CFLAGS
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"; export CXXFLAGS
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
%endif
sh autogen.sh --with-master
%{__make} -f Makefile.meta USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} -f Makefile.meta USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/json-c/*.bc
  %endif
 %endif
%endif

%changelog
* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.8-1
- Update to 5.2.8

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 5.2.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Aug 3 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.7-1
- Update to 5.2.7

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.6-1
- Update to 5.2.6

* Wed May 1 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-1
- Update to 5.2.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Mar 21 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Wed Mar 14 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.2.0

* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
