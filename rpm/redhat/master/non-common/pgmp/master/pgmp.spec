%global sname pgmp

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL Multiple Precision Arithmetic Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.4
Release:	3%{?dist}
License:	LGPL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
# Make sure that we use Python 3.
Patch1:		%{sname}-python3.patch
URL:		https://dvarrazzo.github.io/pgmp/
BuildRequires:	postgresql%{pgmajorversion}-devel gmp-devel pgdg-srpm-macros
Requires:	gmp

Obsoletes:	%{sname}%{pgmajorversion} <= 1.0.4-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
The pgmp extension adds PostgreSQL data types wrapping the high performance
integer and rational data types offered by the GMP library.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
#%%doc %{pginstdir}/doc/%{sname}/*.rst
%doc README.rst
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}*.sql
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.4-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Make sure that we use Python 3.

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jan 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
