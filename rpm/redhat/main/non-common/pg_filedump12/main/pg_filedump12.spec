%global sname pg_filedump
%global sversion REL_12_0

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	12.0
Release:	4%{?dist}
URL:		https://github.com/df7cb/%{sname}
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Source0:	https://github.com/df7cb/pg_filedump/archive/%{sversion}.tar.gz

Obsoletes:	%{sname}%{pgmajorversion} < 12.0-2

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 12.0-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 12.0-3
- Remove pgxs patch, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 12.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Nov 29 2019 Devrim Gündüz <devrim@gunduz.org> - 12.0-1
- Initial packaging for PostgreSQL RPM Repository
