%global sname pllua
%global pname pllua-ng

%global plluangmajver 2
%global plluangmidver 0
%global plluangminver 10

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
Release:	2%{?dist}
License:	MIT
Source0:	https://github.com/RhodiumToad/%{pname}/archive/refs/tags/REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}.tar.gz
URL:		https://github.com/RhodiumToad/%{pname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros lua-devel
Requires:	postgresql%{pgmajorversion}-server lua-libs

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
%{pginstdir}/lib/bitcode/%{sname}*.bc
%dir %{pginstdir}/lib/bitcode/%{sname}
%{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.10-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.10-1
- Update to 2.0.10

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.9-1
- Initial packaging for PostgreSQL RPM Repository
