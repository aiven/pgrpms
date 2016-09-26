%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0
%global sname prefix

Summary:	Prefix Range module for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.2.3
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dimitri/%{sname}/archive/v%{version}.zip
Patch0:		prefix-makefile-pgconfig.patch
URL:		https://github.com/dimitri/prefix
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install
# Move docs under PostgreSQL extensions director
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__mv} %{buildroot}%{_docdir}/pgsql/extension/README.md %{buildroot}%{pginstdir}/share/extension/README-prefix.md
%{__mv} %{buildroot}%{_docdir}/pgsql/extension/TESTS.md %{buildroot}%{pginstdir}/share/extension/TESTS-prefix.md

%clean
rm -rf %{buildroot}

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/share/extension/README-prefix.md
%doc %{pginstdir}/share/extension/TESTS-prefix.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Mon Jan 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.3-1
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
