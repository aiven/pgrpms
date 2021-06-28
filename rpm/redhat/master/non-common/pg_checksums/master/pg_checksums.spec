%global debug_package %{nil}
%global sname pg_checksums

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Activate/deactivate/verify checksums in offline Postgres clusters
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	3%{?dist}
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pg_checksums is based on the pg_verify_checksums and pg_checksums programs
available in PostgreSQL version 11 and from 12, respectively. It cat verify,
activate or deactivate checksums. Activating requires all database blocks to
be read and all page headers to be updated, so can take a long time on a
large database.

The database cluster needs to be shutdown cleanly in the case of checksum
activation or deactivation, while checksum verification can be performed
online, contrary to PostgreSQL's pg_checksums.

Other changes include the possibility to toggle progress reporting via the
SIGUSR1 signal, more fine-grained progress reporting and I/O rate limiting.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%{pginstdir}/bin/%{sname}

%changelog
* Mon Jun 2021 Devrim Gündüz <devrim@gunduz.org> 1.0-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 29 2019 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
