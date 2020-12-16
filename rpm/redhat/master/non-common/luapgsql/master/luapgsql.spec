%global debug_package %{nil}

%global sname luapgsql

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Lua binding for PostgreSQL
Name:		%{sname}
Version:	1.6.7
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/arcapos/%{name}/archive/pgsql-%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/arcapos/%{name}/
BuildRequires:	lua-devel pgdg-srpm-macros
BuildRequires: 	postgresql%{pgmajorversion}-devel lua-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	lua(abi) = %{luaver}
%else
%global luanext 5.2
Requires:	lua >= %{luaver}
Requires:	lua <  %{luanext}
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
A Lua Binding for PostgreSQL.

%prep
%setup -q -n %{sname}-pgsql-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.md
%{lualibdir}/pgsql.so

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.6.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1.1
- Rebuild for PostgreSQL 12

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1
- Update to 1.6.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Aug 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
