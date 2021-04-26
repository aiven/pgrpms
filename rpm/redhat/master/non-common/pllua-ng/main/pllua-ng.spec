%global sname pllua
%global pname pllua-ng

%global plluangmajver 2
%global plluangmidver 0
%global plluangminver 9

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Summary:	Procedural language interface between PostgreSQL and Lua
Name:		%{sname}_%{pgmajorversion}
Version:	%{plluangmajver}.%{plluangmidver}.%{plluangminver}
Release:	1%{?dist}
License:	MIT
Source0:	https://github.com/RhodiumToad/%{pname}/archive/refs/tags/REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}.tar.gz
URL:		https://github.com/RhodiumToad/%{pname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server lua-devel

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PL/Lua is a procedural language module for the PostgreSQL database that
allows server-side functions to be written in Lua.

%package devel
Summary:	PL/Lua development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for PL/Lua

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for PL/Lua
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} == 1315
Requires:       llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:       llvm10
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for PL/Lua
%endif

%prep
%setup -q -n %{pname}-REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

LUA_INCDIR="%{includedir}" LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
LUA_INCDIR="%{includedir}" LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%defattr(644,root,root,755)
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}u*.sql
%{pginstdir}/share/extension/%{sname}u.control

%if %llvm
%files devel
%dir %{pginstdir}/include/server/extension/%{sname}
%{pginstdir}/include/server/extension/%{sname}/*

%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}.index.bc
%{pginstdir}/lib/bitcode/%{sname}*.bc
%dir %{pginstdir}/lib/bitcode/%{sname}
%{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 0.3.0
- Initial packaging for PostgreSQL RPM Repository
