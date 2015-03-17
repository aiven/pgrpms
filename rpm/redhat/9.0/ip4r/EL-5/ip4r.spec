%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0
%global sname ip4r

Name:           %{sname}%{pgmajorversion}
Summary:	IPv4/v6 and IPv4/v6 range index type for PostgreSQL
Version:	2.0.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/RhodiumToad/%{sname}/archive/%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		https://github.com/RhodiumToad/ip4r
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	postgresql-ip4r

%description
ip4, ip4r, ip6, ip6r, ipaddress and iprange are types that contain a single
IPv4/IPv6 address and a range of IPv4/IPv6 addresses respectively. They can
be used as a more flexible, indexable version of the cidr type.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/pgsql/extension/README.ip4r
%{pginstdir}/lib/ip4r.so
%{pginstdir}/share/extension/ip4r*

%changelog
* Wed Jun 11 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2
- Update summary and description

* Sun Sep 15 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0-1
- Update to 2.0, using the "extension" tarball.

* Thu Mar 08 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.05-3
-  Provide postgresql-ip4r, to match the package name in EPEL.

* Tue Oct 12 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.05-2
- Apply 9.0 specific changes to spec file.

* Wed Apr 21 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Mon Sep 7 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.04-1
- Update to 1.04

* Fri Feb 1 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.03-1
- Update to 1.03

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.02-1
- Update to 1.02

* Mon Jul 9 2007 - Devrim GUNDUZ <devrim@gunduz.org> 1.01-2
- Removed unneeded ldconfig calls, per bz review #246747

* Wed Jul 4 2007 - Devrim GUNDUZ <devrim@gunduz.org> 1.01-1
- Initial RPM packaging for Fedora
