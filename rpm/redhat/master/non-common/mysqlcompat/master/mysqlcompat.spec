%global sname mysqlcompat

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	MySQL compatibility functions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.0.7
Release:	2%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

Obsoletes:	%{sname}%{pgmajorversion} <= 0.0.7-1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This project is a collection of functions, aggregates, operators and
casts that make PostgreSQL mimic MySQL as closely as possible.

To use the project, you can either find and install the few functions
that you need, or run all the .sql files to install the complete
compatibility environment.

This can be an immense time-saver when porting large applications that
rely heavily on certain MySQL functions.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.0.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.0.7-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.0.7-1.1
- Rebuild against PostgreSQL 11.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.7-1
- Initial packaging for PostgreSQL RPM Repository
