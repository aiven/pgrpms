%global debug_package %{nil}
%global sname	pg_ivm

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Incremental View Maintenance (IVM) feature for PostgreSQL.
Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}/
Source0:	https://github.com/sraoss/%{sname}/archive/refs/tags/v%{version}.tar.gz

%description
Incremental View Maintenance (IVM) is a way to make materialized views
up-to-date in which only incremental changes are computed and applied on
views rather than recomputing the contents from scratch as REFRESH
MATERIALIZED VIEW does. IVM can update materialized views more efficiently
than recomputation when only small parts of the view are changed.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for XXX
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
This packages provides JIT support for XXX
%endif
%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Update to 1.0

* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-alpha-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
