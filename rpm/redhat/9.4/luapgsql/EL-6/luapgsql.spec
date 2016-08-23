%global pgmajorversion 94
%global pgpackageversion 9.4
%global pginstdir /usr/pgsql-%{pgpackageversion}

%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Lua binding for PostgreSQL
Name:		luapgsql
Version:	1.6.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/arcapos/%{name}/archive/%{version}.tar.gz
Patch0:		luapgsql-makefile.patch
URL:		https://github.com/arcapos/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	lua-devel
BuildRequires: 	postgresql%{pgmajorversion}-devel lua-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	lua(abi) = %{luaver}
%else
%global luanext 5.2
Requires:	lua >= %{luaver}
Requires:	lua <  %{luanext}
%endif

%description
A Lua Binding for PostgreSQL.

%prep
%setup -q
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%{_libdir}/lua/5.3/pgsql.so
%doc README.md

%changelog
* Sun Oct 18 2015 - Devrim Gündüz <devrim@gunduz.org> 1.5-1
- Update to 1.5

* Sun Apr 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4

* Sun Mar 29 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
