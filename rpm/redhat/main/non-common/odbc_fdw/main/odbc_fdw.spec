%global sname	odbc_fdw

%{!?llvm:%global llvm 1}

Summary:	ODBC Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.5.1
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/CartoDB/%{sname}
Source0:	https://github.com/CartoDB/%{sname}/archive/refs/tags/%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW)
for remote databases using Open Database Connectivity (ODBC).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for odbc_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for odbc_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Aug 22 2024 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Initial packaging for the PostgreSQL RPM repositories.
