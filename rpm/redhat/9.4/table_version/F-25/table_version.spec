%global debug_package %{nil}
%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname table_version

Summary:	PostgreSQL table versioning extension
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
# This patch needs an update when next version is released. It includes
# 366f77803cef69d1086a76976842e2544bcc9fef from upstream.
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/table_version/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PostgreSQL table versioning extension, recording row modifications and its
history. The extension provides APIs for accessing snapshots of a table at
certain revisions and the difference generated between any two given revisions.
The extension uses a PL/PgSQL trigger based system to record and provide
access to the row revisions

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/share/extension/table_version*.sql
%{pginstdir}/share/extension/table_version.control

%changelog
* Sun Mar 20 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Initial packaging for PostgreSQL RPM Repository
