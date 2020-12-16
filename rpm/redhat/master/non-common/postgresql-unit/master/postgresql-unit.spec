%global sname postgresql-unit

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	SI Units for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	7.2
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/ChristophBerg/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
postgresql-unit implements a PostgreSQL datatype for SI units, plus byte.
The base units can be combined to named and unnamed derived units using
operators defined in the PostgreSQL type system. SI prefixes are used for
input and output, and quantities can be converted to arbitrary scale.

Requires PostgreSQL 9.5 or later (uses psprintf()), flex, and bison 3 (the
pre-built grammar files are used if only bison 2 is available).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/unit.so
%{pginstdir}/share/extension/unit*.sql
%{pginstdir}/share/extension/unit.control
%{pginstdir}/share/extension/unit_prefixes.data
%{pginstdir}/share/extension/unit_units.data
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/uni*.bc
   %{pginstdir}/lib/bitcode/unit/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 7.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>- 7.2-1.1
- Rebuild for PostgreSQL 12

* Thu Sep 5 2019 Devrim Gündüz <devrim@gunduz.org> 7.2-1
- Update to 7.2

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> 7.1-1
- Update to 7.1

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> 7.0-1
- Update to 7.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 6.0-2.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-2
- Add v11+ bitcode conditionals

* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Sun May 28 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Thu Apr 27 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0
- Add support for Power RPMs.

* Tue Jan 10 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Sep 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
