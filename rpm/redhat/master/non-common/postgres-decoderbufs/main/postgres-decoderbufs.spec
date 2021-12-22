%global sname postgres-decoderbufs

Name:		%{sname}_%{pgmajorversion}
Version:	1.5.2
Release:	1%{?dist}
Summary:	PostgreSQL Protocol Buffers logical decoder plugin

License:	MIT
URL:		https://github.com/debezium/%{sname}

Source0:	https://github.com/debezium/%{sname}/archive/refs/tags/v%{version}.Final.tar.gz

BuildRequires:	gcc llvm clang
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	protobuf-c-devel

Requires:	protobuf-c

%description
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

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
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/decoderbufs*.bc
   %{pginstdir}/lib/bitcode/decoderbufs/src/
  %endif
 %endif
%endif

%changelog
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
