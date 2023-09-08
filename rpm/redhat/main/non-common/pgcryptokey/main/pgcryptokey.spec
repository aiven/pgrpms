%global sname pgcryptokey

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL table versioning extension
Name:		%{sname}_%{pgmajorversion}
Version:	0.85
Release:	5PGDG%{?dist}
License:	BSD
Source0:	http://momjian.us/download/%{sname}/%{sname}-%{version}.tar.gz
URL:		http://momjian.us/download/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.85-2

%description
pgcryptokey allows the creation, selection, rotation, and deletion of
cryptographic data keys. Each cryptographic data key is encrypted/decrypted
with (i.e., wrapped inside) an access password. Accessing a cryptographic
data key requires the proper access password.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgcryptokey
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
This packages provides JIT support for pgcryptokey
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc README
%license LICENSE
%{pginstdir}/lib/%{sname}_acpass.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.0.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_acpass.sample

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}_acpass/*.bc
%endif

%changelog
* Fri Sep 8 2023 Devrim Gunduz <devrim@gunduz.org> - 0.85-5PGDG
- Cleanup rpmlint warnings
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 0.85-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.85-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> 0.85-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.85-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 16 2020 Devrim Gündüz <devrim@gunduz.org> - 0.85-1
- Update to 0.85

* Tue Sep 15 2020 Devrim Gündüz <devrim@gunduz.org> - 0.84-1
- Update to 0.84

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.84-1
- Rebuild for PostgreSQL 12

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 0.83-1
- Initial packaging for PostgreSQL RPM repository.
