%global sname pg_filedump
%global sversion REL_17_0

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	17.1
Release:	1PGDG%{?dist}
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/%{sname}/archive/%{sversion}.tar.gz
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump.md

%changelog
* Sat Nov 9 2024 Devrim Gündüz <devrim@gunduz.org> - 17.1-1PGDG
- Update to 17.1 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_1

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
