%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname ogr_fdw

Summary:	PostgreSQL foreign data wrapper for OGR
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/pramsey/pgsql-ogr-fdw/archive/v%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/pramsey/pgsql-ogr-fdw
BuildRequires:	postgresql%{pgmajorversion}-devel gdal-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with OGR.

%prep
%setup -q -n pgsql-ogr-fdw-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

install -d %{buildroot}%{pginstdir}/
install -d %{buildroot}%{pginstdir}/bin/
install -d %{buildroot}%{pginstdir}/share/extension
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%attr (755,root,root) %{pginstdir}/bin/ogr_fdw_info
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Sep 21 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
