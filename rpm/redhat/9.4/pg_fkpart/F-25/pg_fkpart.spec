%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname pg_fkpart

Summary:	PostgreSQL extension to partition tables following a foreign key
Name:		%{sname}%{pgmajorversion}
Version:	1.5.0
Release:	1%{?dist}
License:	GPLv2
Source0:	https://github.com/lemoineat/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		http://pgxn.org/dist/pg_fkpart/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
pg_fkpart is a PostgreSQL extension to partition tables following a foreign key
of a table.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 %make_install install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc/extension
install -m 644 README.md  %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%changelog
* Sat Aug 13 2016 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.2-1
- Update to 1.2.2
- Move docs to new directory
- Update patch0
- Unified spec file for all platforms.

* Mon May 4 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial packaging
