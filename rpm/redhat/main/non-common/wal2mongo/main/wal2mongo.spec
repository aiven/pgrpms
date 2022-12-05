%global sname wal2mongo

Summary:	PostgreSQL logical decoding output plugin for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.6
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/HighgoSoftware/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/HighgoSoftware/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.6-2

%description
wal2mongo is a PostgreSQL logical decoding output plugin designed to make the
logical replication easier from PostgreSQL to MongoDB by formating the output
to a JSON-like format accepted by mongo.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}/%{pginstdir}/doc/extension/
%{__mv} README.md  %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-3
- Remove pgxs patch, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Jun 2 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Initial RPM packaging for yum.postgresql.org
