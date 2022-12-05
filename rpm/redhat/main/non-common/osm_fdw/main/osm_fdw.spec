%global debug_package %{nil}
%global sname osm_fdw

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL foreign data wrapper OSM PBF
Name:		%{sname}_%{pgmajorversion}
Version:	4.1.2
Release:	2%{?dist}
License:	BSD
Source0:	https://api.pgxn.org/dist/osm_fdw/%{version}/osm_fdw-%{version}.zip
Patch1:		%{sname}-missinginclude.patch
URL:		https://github.com/vpikulik/postgres_osm_pbf_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
%if 0%{?suse_version} >= 1315
BuildRequires:	protobuf-c libprotobuf-c-devel
%else
BuildRequires:	protobuf-c-devel
%endif
Requires:	postgresql%{pgmajorversion}-server, protobuf-c

Obsoletes:	%{sname}_%{pgmajorversion} < 4.0.0-2

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with osm.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for osm_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for osm_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

strip %{buildroot}%{pginstdir}/lib/*.so

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%attr(755,root,root) %{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/osm_reader/*.bc
%endif

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-1
- Update to 4.1.2

* Wed Feb 24 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.1-1
- Update to 4.1.1
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
