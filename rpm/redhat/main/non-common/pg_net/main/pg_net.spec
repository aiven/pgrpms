%global sname pg_net

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension that enables asynchronous (non-blocking) HTTP/HTTPS requests with SQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.9.1
Release:	1PGDG%{?dist}
URL:		https://github.com/supabase/%{sname}
Source0:	https://github.com/supabase/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	Apache-2.0
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The PG_NET extension enables PostgreSQL to make asynchronous HTTP/HTTPS
requests in SQL. It eliminates the need for servers to continuously poll for
database changes and instead allows the database to proactively notify
external resources about significant events. It seamlessly integrates with
triggers, cron jobs (e.g., PG_CRON), and procedures, unlocking numerous
possibilities. Notably, PG_NET powers Supabase's Webhook functionality,
highlighting its robustness and reliability.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_net
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
This packages provides JIT support for pg_net
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
%{pginstdir}/lib/pg_net.so
%{pginstdir}/share/extension/pg_net*.sql
%{pginstdir}/share/extension/pg_net.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Fri May 10 2024 Devrim Gunduz <devrim@gunduz.org> - 0.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository

