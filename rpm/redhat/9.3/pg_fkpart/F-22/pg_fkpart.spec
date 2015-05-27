%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pg_fkpart

Summary:	 PostgreSQL extension to partition tables following a foreign key
Name:		%{sname}%{pgmajorversion}
Version:	1.0
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
rm -rf %{buildroot}

USE_PGXS=1 %make_install install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 644 README.md  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md

%files
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%changelog
* Mon May 4 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial packaging
