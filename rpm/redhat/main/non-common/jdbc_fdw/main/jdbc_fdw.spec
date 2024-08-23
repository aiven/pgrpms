%global sname	jdbc_fdw

%{!?llvm:%global llvm 1}

Summary:	JDBC Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.4.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	https://github.com/pgspider/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pgdg-rpm.patch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} == 9
BuildRequires:	java-17-openjdk-devel
%endif
%if 0%{?rhel} == 8
BuildRequires:	java-latest-openjdk-devel
%endif
%if 0%{?fedora}
BuildRequires:	java-latest-openjdk-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	java-11-openjdk-devel
%endif

%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to
any Java DataBase Connectivity (JDBC) data source.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for jdbc_fdw
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
This packages provides JIT support for jdbc_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

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
* Wed Aug 21 2024 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-1PGDG
- Initial packaging for PostgreSQL RPM repositories. Patch taken from
  Debian sources.
