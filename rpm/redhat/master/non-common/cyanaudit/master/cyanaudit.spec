%if (0%{?fedora})
%global _hardened_build 1
%endif
%global debug_package %{nil}
%global sname cyanaudit

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	DML logging tool for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.2
Release:	1%{?dist}.1
License:	BSD
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/%{sname}
Requires:	postgresql%{pgmajorversion}-plperl
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	protobuf-c libprotobuf-c-devel postgresql%{pgmajorversion}
%endif
%else
BuildRequires:	protobuf-c-devel postgresql%{pgmajorversion}
%endif
BuildRequires:	pgdg-srpm-macros
BuildArch:	noarch

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
Cyan Audit provides in-database logging of all DML activity on a
column-by-column basis.

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
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%clean
%{__rm} -rf %{buildroot}

%files
%if (0%{?fedora} || 0%{?rhel} > 6)
%license LICENSE
%endif
%doc README.md
%defattr(644,root,root,755)
%attr(755, root, -) %{pginstdir}/bin/%{sname}_dump.pl
%attr(755, root, -) %{pginstdir}/bin/%{sname}_log_rotate.pl
%attr(755, root, -) %{pginstdir}/bin/%{sname}_restore.pl
%attr(755, root, -) %{pginstdir}/bin/Cyanaudit.pm
%attr(755, root, -) %{pginstdir}/bin/%{sname}_tablespace_fix.sh
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/*%{sname}*.md

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1.1
- Rebuild against PostgreSQL 11.0

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Wed Mar 9 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0, per #1019.

* Thu Nov 12 2015 - Devrim Gündüz <devrim@gunduz.org> 0.9.5-1
- Update to 0.9.5 .
- Fix various rpmlint errors/warnings.
- Improve %%files section.

* Mon Nov 9 2015 - Devrim Gündüz <devrim@gunduz.org> 0.9.4-3
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Dec 17 2014 - Devrim Gündüz <devrim@gunduz.org> 0.9.4-2
- Add postgresql main package as BR

* Tue Apr 8 2014 - Devrim Gündüz <devrim@gunduz.org> 0.9.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
