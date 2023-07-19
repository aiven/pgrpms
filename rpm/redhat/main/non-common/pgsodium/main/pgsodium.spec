%global sname pgsodium

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension for high level cryptographic algorithms
Name:		%{sname}_%{pgmajorversion}
Version:	3.1.8
Release:	1PGDG%{dist}
License:	BSD
URL:		https://github.com/michelp/%{sname}/
Source0:	https://github.com/michelp/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel libsodium-devel
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?fedora} || 0%{?rhel}
Requires:	libsodium
%endif
%if 0%{?suse_version} >= 1315
Requires:	libsodium23
%endif

%description
pgsodium is an encryption library extension for PostgreSQL using the
libsodium library for high level cryptographic algorithms.

pgsodium can be used a straight interface to libsodium, but it can also use
a powerful feature called Server Key Management where pgsodium loads an
external secret key into memory that is never accessible to SQL. This
inaccessible root key can then be used to derive sub-keys and keypairs by
key id. This id (type bigint) can then be stored instead of the derived key.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsodium
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pgsodium
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Jul 19 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-1PGDG
- Update to 3.1.8
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.7-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon May 29 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.7-1
- Update to 3.1.7

* Tue Apr 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.6-1
- Update to 3.1.6

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4

* Tue Dec 13 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.6-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.6-2
- Fix SLES dependency, per report from Tiago ANASTACIO.
  Fixes https://redmine.postgresql.org/issues/7739

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.6-1
- Update to 3.0.6

* Tue Oct 18 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.5-1
- Update to 3.0.5

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.4-2
- Update SLES 15 dependencies for SP4.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Tue Aug 9 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0

* Tue Feb 15 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
