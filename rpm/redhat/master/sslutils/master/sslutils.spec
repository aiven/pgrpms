%global sname sslutils

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	SSL Utils for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://www.EDBPostgres.com
Source0:	%{sname}-%{version}.tar.bz2
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel, net-snmp-devel
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description
Required extension for Postgres Enterprise Manager (PEM) Server

%prep
%setup -q  -n %{sname}-%{version}
%patch0 -p0

%build

%ifarch ppc64 ppc64le
        CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
        CC=%{atpath}/bin/gcc; export CC
%endif

USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install README-sslutils.txt
%{__install} -d -m 755 %{buildroot}%{pginstdir}/share/doc/extension
%{__cp} README.%{sname} %{buildroot}%{pginstdir}/share/doc/extension/README-%{sname}.txt

%ifarch ppc64 ppc64le
strip %{buildroot}%{pginstdir}/lib/*.so
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
%debug_package
%endif
%endif

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%postun
/sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%attr(644,root,root) %{pginstdir}/share/doc/extension/README-%{sname}.txt
%{pginstdir}/lib/sslutils.so
%{pginstdir}/share/extension/sslutils*.sql
%{pginstdir}/share/extension/uninstall_sslutils.sql
%{pginstdir}/share/extension/sslutils.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against PostgreSQL 11.0

* Fri Feb 23 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial packaging for PostgreSQL RPM repository
