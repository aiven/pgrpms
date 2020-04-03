%global sname prefix

Summary:	Prefix Range module for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.2.9
Release:	1%{?dist}.1
License:	BSD
Source0:	https://github.com/dimitri/%{sname}/archive/v%{version}.zip
Patch0:		prefix-pg%{pgmajorversion}-makefile-pgconfig.patch
URL:		https://github.com/dimitri/prefix
# This is for older spec files (RHEL <= 6)
%if 0%{?rhel} && 0%{?rhel} <= 6
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The prefix project implements text prefix matches operator (prefix @>
text) and provide a GiST opclass for indexing support of prefix
searches.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%make_install DESTDIR=%{buildroot}
# Rename docs to avoid conflict:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-prefix.md
%{__mv} %{buildroot}%{pginstdir}/doc/extension/TESTS.md %{buildroot}%{pginstdir}/doc/extension/TESTS-prefix.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-prefix.md
%doc %{pginstdir}/doc/extension/TESTS-prefix.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
 %endif
%endif

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 - Devrim Gündüz <devrim@gunduz.org> 1.2.9-1
- Update to 1.2.9

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.8-1
- Update to 1.2.8
- Add patches for all supported PostgreSQL releases
- Fix some rpmlint warnings

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4
- Put back Group: tag for RHEL 5.

* Mon Jan 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Omit deprecated Group: tags and %%clean section
- Use %%make_install macro
- No need to cleanup buildroot during %%install
- Remove %%defattr
- Run ldconfig
- Update URL

* Mon Jan 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Mon Jan 7 2013 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix for PostgreSQL 9.0+ RPM layout.

* Fri Dec 11 2009 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Fri May 30 2008 - Devrim Gündüz <devrim@gunduz.org> 0.2-1
- Initial RPM packaging for yum.postgresql.org
