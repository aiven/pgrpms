%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pg_pathman

Summary:	Partitioning tool for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/postgrespro/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The pg_pathman module provides optimized partitioning mechanism and functions
to manage partitions.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p  %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Sep 7 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
