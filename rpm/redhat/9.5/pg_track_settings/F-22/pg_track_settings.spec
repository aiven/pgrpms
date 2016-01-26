%global debug_package %{nil}

%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pg_track_settings

Summary:	PostgreSQL extension to keep track of settings modification
Name:		%{sname}%{pgmajorversion}
Version:	1.0.0
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/rjuju/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/rjuju/pg_track_settings
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_track_settings is a small extension that helps you keep track of
postgresql settings configuration.

It provides a function (pg_track_settings_snapshot()), that me must
called regularly. At each call, it will store the settings that have
been changed since last call. It will also track the postgresql
start time if it's different from the last one.

This extension tracks both overall settings (the pg_settings view)
and overloaded settings (the pg_db_role_setting table).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

#Avoid conflict with some other README file:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Jan 4 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-2
- Update for 9.5 doc layout.

* Thu Jul 23 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
