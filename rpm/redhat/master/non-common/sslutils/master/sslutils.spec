%ifarch ppc64 ppc64le
%global	debug_package %{nil}
%endif

%global sname sslutils

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Summary:	SSL Utils for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	4%{?dist}
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel, net-snmp-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Required extension for Postgres Enterprise Manager (PEM) Server

%prep
%setup -q  -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

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
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif
%endif

%postun
/sbin/ldconfig
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif
%endif

%files
%defattr(-,root,root,-)
%attr(644,root,root) %{pginstdir}/share/doc/extension/README-%{sname}.txt
%{pginstdir}/lib/sslutils.so
%{pginstdir}/share/extension/sslutils*.sql
%{pginstdir}/share/extension/uninstall_sslutils.sql
%{pginstdir}/share/extension/sslutils.control
%if %llvm
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-4
- Disable debug packages on ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-3
- Remove pgxs patches, and export PATH instead.

* Thu Apr 30 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Switch to the new open source repo
- Switch to pgdg-srpm-macros

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against PostgreSQL 11.0

* Fri Feb 23 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial packaging for PostgreSQL RPM repository
