%global sname logerrors

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Extension for PostgreSQL for collecting statistics about messages in logfile
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.2
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/munakoiso/%{sname}
Source0:	https://github.com/munakoiso/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
Extension for PostgreSQL for collecting statistics about messages in logfile

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for logerrors
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
This packages provides JIT support for logerrors
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Jun 4 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2
- Remove patch0, no longer needed.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.1-2.2
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 2.1-2.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Tue Feb 7 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.1-2
- Add a temp patch to install missing .sql file which breaks
  upgrade path to 2.1. Per report from Matej Klonfar.
  https://redmine.postgresql.org/issues/7770#note-4

* Sat Feb 4 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Update to 2.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed May 26 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Mon Aug 3 2020 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
