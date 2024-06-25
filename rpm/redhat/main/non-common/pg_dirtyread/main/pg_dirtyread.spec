%global sname pg_dirtyread

%{!?llvm:%global llvm 1}

Summary:	Read dead but unvacuumed rows from a PostgreSQL relation
Name:		%{sname}_%{pgmajorversion}
Version:	2.7
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/ChristophBerg/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_dirtyread extension provides the ability to read dead but unvacuumed
rows from a relation.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_dirtyread
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pg_dirtyread
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

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif


%changelog
* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7-1PGDG
- Initial RPM packaging for PostgreSQL YUM Repository
