%global sname geoip

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Geolocation using GeoIP for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.2.4
Release:	2%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/geoip/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildArch:	noarch

Obsoletes:	%{sname}_%{pgmajorversion} < 0.2.4-2

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This extension provides IP-based geolocation, i.e. you provide an IPv4 address
and the extension looks for info about country, city, GPS etc.

To operate, the extension needs data mapping IP addresses to the other info,
but these data are not part of the extension. A good free dataset is GeoLite
from MaxMind (available at www.maxmind.com).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/uninstall_%{sname}.sql

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.2.4-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.2.4-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2.4-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 10 2015 - Devrim Gündüz <devrim@gunduz.org> 0.2.4-1
- Update to 0.2.4

* Wed Jan 21 2015 - Devrim Gündüz <devrim@gunduz.org> 0.2.3-1
- Initial packaging for PostgreSQL RPM Repository
