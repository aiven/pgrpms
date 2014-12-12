%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname mysql_fdw

Summary:	PostgreSQL  Foreign Data Wrapper (FDW) for the MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-1_0_1.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/mysql_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel, mysql-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
the MySQL.

%prep
%setup -q -n %{sname}-REL-1_0_1
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README %{buildroot}%{pginstdir}/share/extension/README-%{sname}
rm -f %{buildroot}%{_docdir}/pgsql/extension/README

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri Oct 10 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
