%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname mongo_fdw

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}%{pgmajorversion}
Version:	3.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/mongo_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
MongoDB. 

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
rm -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc LICENSE
%{pginstdir}/lib/mongo_fdw.so
%{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/mongo_fdw--1.0.sql
%{pginstdir}/share/extension/mongo_fdw.control

%changelog
* Sun Sep 7 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
