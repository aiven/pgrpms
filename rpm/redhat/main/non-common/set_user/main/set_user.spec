%global sname	set_user

%global setusermajver 4
%global setusermidver 0
%global setuserminver 1

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension allowing privilege escalation with enhanced logging and control
Name:		%{sname}_%{pgmajorversion}
Version:	%{setusermajver}.%{setusermidver}.%{setuserminver}
Release:	2%{?dist}.1
License:	PostgreSQL
URL:		https://github.com/pgaudit/%{sname}
Source0:	https://github.com/pgaudit/%{sname}/archive/refs/tags/REL%{setusermajver}_%{setusermidver}_%{setuserminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension allows switching users and optional privilege
escalation with enhanced logging and control. It provides an additional layer
of logging and control when unprivileged users must escalate themselves to
superuser or object owner roles in order to perform needed maintenance tasks.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for set_user
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
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
This packages provides JIT support for set_user
%endif

%prep
%setup -q -n %{sname}-REL%{setusermajver}_%{setusermidver}_%{setuserminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

# Remove header file, we don't need to ship it:
%{__rm} -f %{buildroot}%{pginstdir}/include/%{sname}.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/src/%{sname}*.bc
    %{pginstdir}/lib/bitcode/src/%{sname}/src/%{sname}.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org>
- Rebuild against LLVM 15 on SLES 15

* Wed Feb 22 2023 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Update to 4.0.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Tue Aug 31 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
