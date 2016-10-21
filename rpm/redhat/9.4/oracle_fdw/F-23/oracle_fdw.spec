%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname	oracle_fdw
%global ofdwmajver 1
%global ofdwmidver 5
%global ofdwminver 0

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

Summary:	A PostgreSQL Foreign Data Wrapper for Oracle.
Name:		%{sname}%{pgmajorversion}
Version:	%{ofdwmajver}.%{ofdwmidver}.%{ofdwminver}
Release:	1%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://laurenz.github.io/oracle_fdw/
Source0:	https://github.com/laurenz/oracle_fdw/archive/ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}.tar.gz
Patch0:		oracle_fdw-makefile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
# Package builder needs to adjust this as needed.
#BuildRequires:	oracle-instantclient11.2-basic
#BuildRequires:	oracle-instantclient11.2-devel
Requires:	postgresql%{pgmajorversion}-server
#Requires:	oracle-instantclient11.2-basic

# Override RPM dependency generation to filter out libclntsh.so.
# http://fedoraproject.org/wiki/PackagingDrafts/FilteringAutomaticDependencies
%global		_use_internal_dependency_generator 0

%description
Provides a Foreign Data Wrapper for easy and efficient read access from
PostgreSQL to Oracle databases, including pushdown of WHERE conditions and
required columns as well as comprehensive EXPLAIN support.

%prep
%setup -q -n %{sname}-ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}
%patch0 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if %runselftest
make installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres PGPORT=5495
%endif

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README.%{sname}

%changelog
* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0
- Put check into conditional, and disable it by default.
- Update for new doc layout.

* Tue Feb 3 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Add a patch for PGXS compilation.
- Ran dos2unix against the spec file, to fix build issues.

* Thu Dec 26 2013 Devrim Gündüz <devrim@gunduz.org> 0.9.10-1
- Update to 0.9.10-1

* Mon Oct 8 2012 David E. Wheeler <david.wheeler@iovation.com> 0.9.7-1
- Initial RPM
 
