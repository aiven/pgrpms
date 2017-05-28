%global sname postcode
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	UK postcode type optimised for indexing
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	1%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/postcode/%{version}/postcode-%{version}.zip
Patch0:		%{sname}-1.3.0-c99.patch
Patch1:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://pgxn.org/dist/postcode/
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
UK postcode encoded in 32 bits and optimised for indexing and partial matches.
Parses and encodes UK postcodes in 32 bits optimised for indexing and partial
matches. Also provides suitable type for delivery point suffixes.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} %{?_smp_mflags}

%install
%make_install
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
# Install sql/ directory:
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}/
%{__cp} -rp sql/ %{buildroot}/%{_datadir}/%{name}/

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{_datadir}/%{name}

%changelog
* Tue May 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
