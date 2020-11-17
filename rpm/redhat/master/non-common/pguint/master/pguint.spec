%global sname pguint

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Unsigned and other extra integer types for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20200704
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch1:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/petere/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <2 1.20200704-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This extension provides additional integer types for PostgreSQL:

* int1 (signed 8-bit integer)
* uint1 (unsigned 8-bit integer)
* uint2 (unsigned 16-bit integer)
* uint4 (unsigned 32-bit integer)
* uint8 (unsigned 64-bit integer)

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/lib/uint.so
%{pginstdir}/share/extension/uint*
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/uint*.bc
   %{pginstdir}/lib/bitcode/uint/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-1
- Initial RPM packaging for PostgreSQL YUM Repository
