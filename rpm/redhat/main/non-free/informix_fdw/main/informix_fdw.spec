%global sname	informix_fdw
%global ifxfdwmajver 0
%global ifxfdwmidver 5
%global ifxfdwminver 3

Summary:	A PostgreSQL Foreign Data Wrapper for Informix
Name:		%{sname}_%{pgmajorversion}
Version:	%{ifxfdwmajver}.%{ifxfdwmidver}.%{ifxfdwminver}
Release:	2%{?dist}
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
#BuildRequires:	some-informix-dependency maybe?
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.5.3-2

%description
The PostgreSQL Informix Foreign Datawrapper (FDW) module is a driver
for accessing remote Informix table from within PostgreSQL databases.
Foreign Tables are transparently accessed as normal PostgreSQL tables,
they can be used to join remote data against real PostgreSQL tables,
import remote data and more.

%prep
%setup -q -n %{sname}-REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}
%patch -P 0 -p0

%build
PATH=/opt/IBM/informix/bin:$PATH INFORMIXDIR=/opt/IBM/informix USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.5.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-1
- Update to 0.5.3

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.2-1
- Update to 0.5.2

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Update to 0.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 25 2016 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Initial packaging for PostgreSQL RPM repository.
