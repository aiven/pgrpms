%global sname	login_hook

%{!?llvm:%global llvm 1}

Summary:	Postgres database extension to execute some code on user login, comparable to Oracle's after logon trigger.
Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	1PGDG%{?dist}
License:	GPLv3
URL:		https://github.com/splendiddata/%{sname}
Source0:	https://github.com/splendiddata/%{sname}/archive/refs/tags/version_%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres database extension to execute some code on user login,
comparable to Oracle's after logon trigger.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for login_hook
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for login_hook
%endif

%prep
%setup -q -n %{sname}-version_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
# No need to ship these files:
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.css
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.html

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Oct 30 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-1PGDG
- Initial packaging for PostgreSQL RPM Repository
