%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname tds_fdw

Summary:	TDS Foreign Data Wrapper for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.5
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/geoip/
BuildRequires:	postgresql%{pgmajorversion}-devel, freetds-devel
Requires:	postgresql%{pgmajorversion}-server, freetds
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library contains a single PostgreSQL extension, a foreign data wrapper
called "tds_fdw". It can be used to communicate with Microsoft SQL
Server and Sybase databases.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 644 README.md  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}/%{_docdir}/pgsql/extension/README.%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%changelog
* Fri Sep 25 2015  - Devrim GUNDUZ <devrim@gunduz.org> 1.0.5-1
- Initial packaging for PostgreSQL RPM Repository
