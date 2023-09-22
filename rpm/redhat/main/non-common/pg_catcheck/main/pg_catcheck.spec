%global sname pg_catcheck

Summary:	Tool for diagnosing PostgreSQL system catalog corruption
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/EnterpriseDB/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.0-2

%description
pg_catcheck is a simple tool for diagnosing system catalog corruption.
If you suspect that your system catalogs are corrupted, this tool may
help you figure out exactly what problems you have and how serious they
are. If you are paranoid, you can run it routinely to search for system
catalog corruption that might otherwise go undetected. However, pg_catcheck
is not a general corruption detector. For that, you should use PostgreSQL's
checksum feature (`initdb -k`).

%prep
%setup -q -n %{sname}-%{version}

%build
export CFLAGS="${CFLAGS} -flto"
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%license LICENSE
%{pginstdir}/bin/%{sname}
%{pginstdir}/doc/README-%{sname}.md

%changelog
* Fri Sep 22 2023 Devrim Gündüz <devrim@gunduz.org> 1.4.0-1PGDG
- Update to 1.4.0
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Feb 1 2022 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 1.2.0-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.2.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Sep 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Dec 12 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0
* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
