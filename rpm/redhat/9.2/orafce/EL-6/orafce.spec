%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname orafce
%global orafcemajver 3
%global orafcemidver 3
%global orafceminver 0

Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	%{orafcemajver}.%{orafcemidver}.%{orafceminver}
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{sname}/%{sname}/archive/VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}.tar.gz
Patch0:		%{sname}-makefile.patch
Patch1:		%{sname}.control.patch
URL:		https://github.com/orafce/orafce
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel, krb5-devel, bison, flex
Requires:	postgresql%{pgmajorversion}

%description
The goal of this project is implementation some functions from Oracle database.
Some date functions (next_day, last_day, trunc, round, ...) are implemented
now. Functionality was verified on Oracle 10g and module is useful
for production work.

%prep
%setup -q -n %{sname}-VERSION_%{orafcemajver}_%{orafcemidver}_%{orafceminver}
%patch0 -p0
%patch1 -p0

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

USE_PGXS=1 make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/COPYRIGHT.orafce
%doc %{pginstdir}/doc/extension/INSTALL.orafce
%doc %{pginstdir}/doc/extension/README.asciidoc
%{pginstdir}/lib/orafce.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/orafce--*.sql

%changelog
* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Fri Feb 19 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1

* Mon Jul 13 2015 - Devrim GUNDUZ <devrim@gunduz.org> 3.1.2-1
- Update to 3.1.2

* Tue Jan 20 2015 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.14-1
- Update to 3.0.14

* Wed Oct 22 2014 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.7-1
- Update to 3.0.7

* Thu Sep 13 2012 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Fri Oct 2 2009 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Remove patch0, it is in upstream now.
- Apply some 3.0 fixes to spec.

* Wed Aug 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.3-2
- Spec file fixes, per bz review #251805

* Mon Jan 14 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Fri Aug 10 2007 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.1-1
- Initial packaging
