%global debug_package %{nil}
%global sname db2_fdw

Summary:	PostgreSQL DB2 Foreign Data Wrapper
Name:		%{sname}%{pgmajorversion}
Version:	2.0.1
Release:	1%{?dist}
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/wolfgangbrandl/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
db2_fdw is a PostgreSQL extension that provides a Foreign Data Wrapper for
easy and efficient access to DB2 databases, including pushdown of WHERE
conditions and required columns as well as comprehensive EXPLAIN support.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
export DB2_HOME="/opt/ibm/db2/V11.5/"
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make}  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/lib/%{sname}.so
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
* Sat Nov 23 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial packaging for PostgreSQL non-free RPM Repository
