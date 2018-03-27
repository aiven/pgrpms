%global sname hll

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL extension adding HyperLogLog data structures as a native data type
Name:		%{sname}_%{pgmajorversion}
Version:	2.10.2
Release:	1%{dist}
License:	Apache
Group:		Applications/Databases
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This Postgres module introduces a new data type hll which is a
HyperLogLog data structure. HyperLogLog is a fixed-size, set-like
structure used for distinct value counting with tunable precision. For
example, in 1280 bytes hll can estimate the count of tens of billions of
distinct values with only a few percent error.

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.markdown %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.markdown
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Mar 27 2018 -  Devrim Gündüz <devrim@gunduz.org> 2.10.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
