%global sname	pljava
%global relver	1_6_5

%global debug_package %{nil}

%ifarch ppc64 ppc64le
%global archtag	ppc64le
%else
%global	archtag	amd64
%endif

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.6.5
Release:	1PGDG%{?dist}
License:	BSD
URL:		http://tada.github.io/%{sname}/

Source0:	https://github.com/tada/%{sname}/archive/V%{relver}.tar.gz
Source1:	%{sname}.pom

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	java-1_8_0-openjdk-devel
Requires:	java-1_8_0-openjdk-headless
%endif
%else
BuildRequires:	java-1.8.0-openjdk-devel
Requires:	java-headless >= 1:1.8
%endif

BuildRequires:	pgdg-srpm-macros
BuildRequires:	openssl-devel krb5-devel

%if 0%{?rhel} == 7
BuildRequires:	rh-maven33
%endif

Obsoletes:	%{sname}-%{pgmajorversion} < 1.5.6-2

%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -q -n %{sname}-%{relver}

%build
export CLASSPATH=

%if 0%{?rhel} && 0%{?rhel} == 7
export PATH=%{atpath}/bin/:$PATH
%endif

%ifarch ppc64 ppc64le
# The next line is useful only on RHEL 7, for the rh-maven33 package
export PATH=%{pginstdir}/bin
mvn clean install -Dso.debug=true -Psaxon-examples -Dnar.aolProperties=pljava-so/aol.%{archtag}-linux-gpp.properties
%else
# The next line is useful only on RHEL 7, for the rh-maven33 package
export PATH=%{pginstdir}/bin:/opt/rh/rh-maven33/root/usr/bin:$PATH
# ommon for all distros:
mvn clean install -Dso.debug=true -Psaxon-examples
%endif

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/lib
%{__cp} -f ./pljava-so/target/pljava-pgxs/libpljava-so-%{version}.so %{buildroot}%{pginstdir}/lib

%{__install} -d %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}/target/%{sname}-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-examples/target/%{sname}-examples-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-api/target/%{sname}-api-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--%{version}.sql
%{__cp} -f %{sname}-packaging/target/classes/%{sname}--unpackaged.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql

%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.control %{buildroot}%{pginstdir}/share/extension

%files
%doc README.md
%license COPYRIGHT
%{pginstdir}/lib/libpljava-so-%{version}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}--1*.sql
%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql
%{pginstdir}/share/%{sname}/%{sname}-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-examples-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-api-%{version}.jar

%changelog
* Mon Aug 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1PGDG
- Update to 1.6.5
- Add PGDG branding
- Fix rpmlint warning

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Feb 15 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.6.4-1
- Update to 1.6.4

* Mon Oct 11 2021 - Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1
- Update to 1.6.3

* Tue Sep 21 2021 - Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1
- Update to 1.6.2
- Remove patch0, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.5.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 6 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.5.6-1
- Update to 1.5.6

* Fri Jul 10 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.5.5-1
- Update to 1.5.5
- Add ppc64le support

* Tue Apr 28 2020 - John Harvey <john.harvey@crunchydata.com> - 1.5.4-1
- Update to 1.5.4

* Sat Oct 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Create symlinks of .sql files for extension updates. Per Chapman.

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-b1_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 20 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.1-b1-1
- Update to 1.5.1 Beta 1

* Tue Mar 28 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.0-2
- Fix packaging, per EnterpriseDB's spec file.

* Thu Jul 14 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Tue Feb 23 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0beta2-1
- Initial packaging for PostgreSQL RPM repository
