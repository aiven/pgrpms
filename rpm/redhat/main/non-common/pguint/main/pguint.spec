%global sname pguint

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Unsigned and other extra integer types for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20220601
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/petere/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <= 1.20200704-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This extension provides additional integer types for PostgreSQL:

* int1 (signed 8-bit integer)
* uint1 (unsigned 8-bit integer)
* uint2 (unsigned 16-bit integer)
* uint4 (unsigned 32-bit integer)
* uint8 (unsigned 64-bit integer)

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pguint
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} == 1315
Requires:	llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:	llvm10
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for pguint
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/lib/uint.so
%{pginstdir}/share/extension/uint*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/uint.index.bc
    %{pginstdir}/lib/bitcode/uint/*.bcaggregates.bc
%endif

%changelog
* Wed Jun 1 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220601-2
- Split llvmjit into its own subpackage, which also will fix
  RHEL 8 - ppc64le builds.

* Wed Jun 1 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220601-1
- Update to 1.20220601

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-1
- Initial RPM packaging for PostgreSQL YUM Repository
