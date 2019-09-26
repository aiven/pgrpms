%global full_version %{version}.Final
%global sname postgres-decoderbufs

Name:		%{sname}_%{pgmajorversion}
Version:	0.9.5
Release:	1%{?dist}.1
Summary:	PostgreSQL Protocol Buffers logical decoder plugin

License:	MIT
URL:		https://github.com/debezium/postgres-decoderbufs

Source0:	https://github.com/debezium/%{sname}/archive/v%{full_version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch

BuildRequires:	gcc
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgis-devel >= 2
BuildRequires:	protobuf-c-devel

Requires:	protobuf-c

Recommends:	postgis

%description
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

%prep
%setup -qn postgres-decoderbufs-%{full_version}
%patch0 -p0

%build
%make_build

%install
%make_install


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
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue May 14 2019 - Jiri Pechanec <jpechane@redhat.com> 0.9.5-1
- Initial RPM packaging
