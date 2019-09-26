%global sname pldebugger

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}%{pgmajorversion}
Version:	1.1
Release:	1%{?dist}.1
Summary:	PL/pgSQL debugger server-side code
License:	Artistic  2.0
URL:		https://git.postgresql.org/gitweb/?p=%{sname}.git;a=summary
Source0:	%{sname}-%{version}.tar.bz2
Source1:	%{sname}.LICENSE
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
This module is a set of shared libraries which implement an API for
debugging PL/pgSQL functions on PostgreSQL 8.4 and above. The pgAdmin
project (http://www.pgadmin.org/) provides a client user interface as
part of pgAdmin III v1.10.0 and above, and pgAdmin 4.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%{__cp} -p %{SOURCE1} ./LICENSE

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 644 README.%{sname} %{buildroot}%{pginstdir}/doc/extension/README.%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README.%{sname}
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README.%{sname}
%license LICENSE
%endif
%{pginstdir}/lib/plugin_debugger.so
%{pginstdir}/share/extension/pldbgapi*.sql
%{pginstdir}/share/extension/pldbgapi*.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/plugin_debugger*.bc
   %{pginstdir}/lib/bitcode/plugin_debugger/*.bc
  %endif
 %endif
%endif


%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jun 5 2017 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL YUM repository.

