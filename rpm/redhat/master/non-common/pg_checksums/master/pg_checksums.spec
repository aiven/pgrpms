%global debug_package %{nil}
%global sname pg_checksums

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Activate/deactivate/verify checksums in offline Postgres clusters
Name:		%{sname}%{pgmajorversion}
Version:	1.0
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
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
pg_checksums is based on the pg_verify_checksums and pg_checksums programs
available in PostgreSQL version 11 and from 12, respectively. It cat verify,
activate or deactivate checksums. Activating requires all database blocks to
be read and all page headers to be updated, so can take a long time on a
large database.

The database cluster needs to be shutdown cleanly in the case of checksum
activation or deactivation, while checksum verification can be performed
online, contrary to PostgreSQL's pg_checksums.

Other changes include the possibility to toggle progress reporting via the
SIGUSR1 signal, more fine-grained progress reporting and I/O rate limiting.

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
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/bin/%{sname}

%changelog
* Tue Oct 29 2019 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
