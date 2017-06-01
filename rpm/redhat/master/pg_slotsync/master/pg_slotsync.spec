%global sname pg_slotsync
%global fname pg_slotcontrol

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}%{pgmajorversion}
Version:	1.0
Release:	1%{?dist}
Summary:	Script and extension to keep replication slot in sync between master and replicas
License:	PostgreSQL
URL:		https://github.com/mhagander/%{sname}
Source0:	https://github.com/mhagander/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pg_slotcontrol provides a simple extension for controlling the position
of a replication slot. It allows moving the position that the
replication slot reserves, to make sure it doesn't block WAL
unnecessarily. Note that actually using this on a logical replication
slot is likely to break the replication apply, but for a physical slot
it is safe as long as the WAL is archived elsewhere.

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
pushd %{fname}
%{__make} %{?_smp_mflags}
popd

%install
%{__rm} -rf %{buildroot}
pushd %{fname}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
popd
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 %{fname}/README.md %{buildroot}%{pginstdir}/doc/extension/%{sname}-README.md

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%doc %{pginstdir}/doc/extension/%{sname}-README.md
%else
%doc %{pginstdir}/doc/extension/%{sname}-README.md
%license LICENSE
%endif
%{pginstdir}/lib/%{fname}.so
%{pginstdir}/share/extension/%{fname}.control
%{pginstdir}/share/extension/%{fname}*sql

%changelog
* Thu May 4 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL YUM repository.
