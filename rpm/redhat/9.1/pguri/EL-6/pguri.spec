%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pguri

Summary:	uri type for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.20150415
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch1:		%{sname}-makefile.patch
URL:		https://github.com/petere/pguri
BuildRequires:	postgresql%{pgmajorversion}-devel, uriparser-devel
Requires:	postgresql%{pgmajorversion}-server, uriparser
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
%patch1 -p0

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/lib/uri.so
%{pginstdir}/share/extension/uri--0.sql
%{pginstdir}/share/extension/uri.control

%changelog
* Fri Apr 17 2015 - Devrim Gündüz <devrim@gunduz.org> 1.20150415-1
- Initial RPM packaging for PostgreSQL YUM Repository
