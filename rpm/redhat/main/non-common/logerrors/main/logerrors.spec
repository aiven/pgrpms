%global sname logerrors

%{!?llvm:%global llvm 1}

Summary:	Extension for PostgreSQL for collecting statistics about messages in logfile
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.3
Release:	1PGDG%{?dist}
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
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
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
* Fri Aug 23 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1PGDG
- Update to 2.1.3 per changes described at:
  https://github.com/munakoiso/logerrors/releases/tag/v2.1.3

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Feb 22 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.2-2PGDG
- Add PGDG branding

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
