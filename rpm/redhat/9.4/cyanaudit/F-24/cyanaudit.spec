%if (0%{?fedora})
%global _hardened_build 1
%endif
%global debug_package %{nil}
%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname cyanaudit

Summary:	DML logging tool for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		cyanaudit-makefile-pgconfig.patch
URL:		http://pgxn.org/dist/cyanaudit
Requires:	postgresql%{pgmajorversion}-plperl
BuildRequires:	protobuf-c-devel, postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
Cyan Audit provides in-database logging of all DML activity on a
column-by-column basis.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%clean
%{__rm} -rf %{buildroot}

%files
%if (0%{?fedora} || 0%{?rhel} > 6)
%license LICENSE
%endif
%doc README.md
%defattr(644,root,root,755)
%attr(755, root, -) %{pginstdir}/bin/cyanaudit_dump.pl
%attr(755, root, -) %{pginstdir}/bin/cyanaudit_log_rotate.pl
%attr(755, root, -) %{pginstdir}/bin/cyanaudit_restore.pl
%attr(755, root, -) %{pginstdir}/bin/Cyanaudit.pm
%attr(755, root, -) %{pginstdir}/bin/cyanaudit_tablespace_fix.sh
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/cyanaudit.control
%{pginstdir}/doc/extension/*cyanaudit*.md

%changelog
* Wed Mar 9 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0, per #1019.

* Thu Nov 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.9.5-1
- Update to 0.9.5 .
- Fix various rpmlint errors/warnings.
- Improve %%files section.

* Mon Nov 9 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.9.4-3
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Dec 17 2014 - Devrim GUNDUZ <devrim@gunduz.org> 0.9.4-2
- Add postgresql main package as BR

* Tue Apr 8 2014 - Devrim GUNDUZ <devrim@gunduz.org> 0.9.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
