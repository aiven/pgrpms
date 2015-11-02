%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname	plv8

Summary:	 V8 Engine Javascript Procedural Language add-on for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		https://github.com/plv8/plv8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, v8-devel >= 3.14.5, gcc-c++
Requires:	postgresql%{pgmajorversion}, v8 >= 3.14.5

%description
plv8 is a shared library that provides a PostgreSQL procedural language
powered by V8 JavaScript Engine. With this program you can write in JavaScript
your function that is callable from SQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot} %{?_smp_mflags}
%{__rm} -f  %{buildroot}%{_datadir}/*.sql

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT README Changes doc/%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/plcoffee--%{version}.sql
%{pginstdir}/share/extension/plcoffee.control
%{pginstdir}/share/extension/plls--%{version}.sql
%{pginstdir}/share/extension/plls.control
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Jul 23 2015 Devrim Gündüz <devrim@gunduz.org> 1.4.4-1
- Update to 1.4.4
- Update URL

* Wed Jul 9 2014 Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Dec 12 2013 Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Initial spec file, per RH #1036130, after doing modifications
  to suit community RPM layout. Original work is by David
  Wheeler and Mikko Tiihonen
