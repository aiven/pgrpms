%global sname postgres-decoderbufs

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.4.0
Release:	1PGDG%{?dist}
Summary:	PostgreSQL Protocol Buffers logical decoder plugin

License:	MIT
URL:		https://github.com/debezium/%{sname}

Source0:	https://github.com/debezium/%{sname}/archive/refs/tags/v%{version}.Final.tar.gz

BuildRequires:	gcc
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?suse_version} >= 1315
BuildRequires:	libprotobuf-c-devel
Requires:	libprotobuf-c1
%else
BuildRequires:	protobuf-c-devel
Requires:	protobuf-c
%endif

%description
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgres-decoderbufs
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for postgres-decoderbufs
%endif
%prep
%setup -qn %{sname}-%{version}.Final

%build
PATH=%{pginstdir}/bin/:$PATH %make_build

%install
PATH=%{pginstdir}/bin/:$PATH %make_install

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/decoderbufs.so
%{pginstdir}/share/extension/decoderbufs.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/decoderbufs*.bc
   %{pginstdir}/lib/bitcode/decoderbufs/src/
%endif

%changelog
* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
- Add SLES 15 support

* Fri Jul 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0
- Add PGDG branding

* Thu May 25 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Feb 22 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Update to 1.7.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2
- Remove pgxs patches, and export PATH instead.

* Thu Jan 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Drop PostGIS BR

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue May 14 2019 - Jiri Pechanec <jpechane@redhat.com> 0.9.5-1
- Initial RPM packaging
