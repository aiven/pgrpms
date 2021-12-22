%global sname pguri

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	uri type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20151224
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/petere/pguri
BuildRequires:	postgresql%{pgmajorversion}-devel, uriparser-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server, uriparser

Obsoletes:	%{sname}%{pgmajorversion} < 1.20151224-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This is an extension for PostgreSQL that provides a uri data type. Advantages
over using plain text for storing URIs include:

 * URI syntax checking
 * functions for extracting URI components
 * human-friendly sorting

The actual URI parsing is provided by the uriparser library, which supports
URI syntax as per RFC 3986.

Note that this might not be the right data type to use if you want to store
user-provided URI data, such as HTTP referrers, since they might contain
arbitrary junk.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/lib/uri.so
%{pginstdir}/share/extension/uri-*.sql
%{pginstdir}/share/extension/uri.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/uri*.bc
   %{pginstdir}/lib/bitcode/uri/*.bc
  %endif
 %endif
%endif


%changelog
* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20151224-1
- Update to 1.20151224

* Fri Apr 17 2015 - Devrim Gündüz <devrim@gunduz.org> 1.20150415-1
- Initial RPM packaging for PostgreSQL YUM Repository
