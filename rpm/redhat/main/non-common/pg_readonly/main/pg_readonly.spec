%global sname pg_readonly

Summary:	PostgreSQL extension which allows to set all cluster databases read only.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.3
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/pierreforstmann/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
pg_readonly is a PostgreSQL extension which allows to set all cluster
databases read only.

The read-only status is managed only in (shared) memory with a global flag.
SQL functions are provided to set the flag, to unset the flag and to query
the flag. The current version of the extension does not allow to store the
read-only status in a permanent way.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file.
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Nov 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
