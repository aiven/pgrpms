%global sname mongo_fdw
%global relver 5_0_0

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}%{pgmajorversion}
Version:	5.0.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{relver}.tar.gz
Source1:	%{sname}-config.h
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/mongo_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	mongo-c-driver libbson
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
MongoDB.

%prep
%setup -q -n %{sname}-REL-%{relver}
%patch0 -p0
%{__cp} %{SOURCE1} ./config.h

%build
%{__make} -f Makefile.meta USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

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
* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.0.0

* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
