%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname prefix

Summary:	Prefix Range module for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.2.4
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/dimitri/%{sname}/archive/v%{version}.zip
Patch0:		prefix-makefile-pgconfig.patch
URL:		https://github.com/dimitri/prefix
# This is for older spec files (RHEL <= 6)
%if 0%{?rhel} && 0%{?rhel} <= 6
Group:		Application/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%make_install DESTDIR=%{buildroot}
# Rename docs to avoid conflict:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-prefix.md
%{__mv} %{buildroot}%{pginstdir}/doc/extension/TESTS.md %{buildroot}%{pginstdir}/doc/extension/TESTS-prefix.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%%doc %{pginstdir}/doc/extension/README-prefix.md
%%doc %{pginstdir}/doc/extension/TESTS-prefix.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Thu Mar 3 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4
- Put back Group: tag for RHEL 5.

* Mon Jan 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.3-1
- Omit deprecated Group: tags and %%clean section
- Use %%make_install macro
- Get rid of BuildRoot definition
- No need to cleanup buildroot during %%install
- Remove %%defattr
- Run ldconfig
- Update URL

* Mon Jan 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Mon Jan 7 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix for PostgreSQL 9.0+ RPM layout.

* Fri Dec 11 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Fri May 30 2008 - Devrim GUNDUZ <devrim@gunduz.org> 0.2-1
- Initial RPM packaging for yum.postgresql.org
