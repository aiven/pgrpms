%global pname pgsql_http
%global sname pgsql-http

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL HTTP client
Name:		%{pname}_%{pgmajorversion}
Version:	1.6.0
Release:	1PGDG%{?dist}
URL:		https://github.com/pramsey/%{sname}
Source0:	https://github.com/pramsey/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pgsql_http allows users to be able to write a trigger that calls a
web service either to get back a result, or to poke that service into
refreshing itself against the new state of the database.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsql_http
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif

%description llvmjit
This packages provides JIT support for pgsql_http
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/http.so
%{pginstdir}/share/extension/http*.sql
%{pginstdir}/share/extension/http*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/http.index*.bc
    %{pginstdir}/lib/bitcode/http/*.bc
%endif

%changelog
* Fri Apr 5 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

