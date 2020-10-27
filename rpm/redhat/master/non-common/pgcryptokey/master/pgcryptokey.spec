%global sname pgcryptokey

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL table versioning extension
Name:		%{sname}_%{pgmajorversion}
Version:	0.85
Release:	2%{?dist}
License:	BSD
Source0:	http://momjian.us/download/%{sname}/%{sname}-%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://momjian.us/download/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <= 0.85-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgcryptokey allows the creation, selection, rotation, and deletion of
cryptographic data keys. Each cryptographic data key is encrypted/decrypted
with (i.e., wrapped inside) an access password. Accessing a cryptographic
data key requires the proper access password.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README
%license LICENSE
%{pginstdir}/lib/%{sname}_acpass.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.0.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_acpass.sample

%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}_acpass/*.bc
  %endif
 %endif
%endif

%changelog
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
