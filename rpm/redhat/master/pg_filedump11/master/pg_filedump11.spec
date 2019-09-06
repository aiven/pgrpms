%global sname pg_filedump
%global sversion REL_11_0

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}%{pgmajorversion}
Version:	11.0
Release:	1%{?dist}
URL:		https://github.com/ChristophBerg/%{sname}
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel

Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{sversion}.tar.gz
Patch1:		pg_filedump-pg%{pgmajorversion}-makefile-pgxs.patch

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump

%changelog
* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 11.0-1
- Initial packaging for PostgreSQL RPM Repository
