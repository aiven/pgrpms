%global sname		pljava
%global debug_package %{nil}
%ifarch ppc64 ppc64le
%global archtag	ppc64le
%else
%global	archtag	amd64
%endif

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	1.5.5
Release:	1%{?dist}
License:	BSD
URL:		http://tada.github.io/%{sname}/
Patch0:		%{sname}-pg%{pgmajorversion}-buildxml.patch

Source0:	https://github.com/tada/%{sname}/archive/V1_5_5.tar.gz
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

BuildRequires:	maven pgdg-srpm-macros
BuildRequires:	openssl-devel krb5-devel

%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -q -n %{sname}-1_5_5
%patch0 -p0

%build
export CLASSPATH=

%ifarch ppc64 ppc64le
export PATH=%{atpath}/bin/:$PATH
mvn clean install -Dso.debug=true -Psaxon-examples -Dnar.aolProperties=pljava-so/aol.%{archtag}-linux-gpp.properties
%else
mvn clean install -Dso.debug=true -Psaxon-examples
%endif

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/lib
%{__cp} -f %{sname}-so/target/nar/%{sname}-so-%{version}-%{archtag}-Linux-gpp-plugin/lib/%{archtag}-Linux-gpp/plugin/libpljava-so-%{version}.so %{buildroot}%{pginstdir}/lib

%{__install} -d %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}/target/%{sname}-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-examples/target/%{sname}-examples-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-api/target/%{sname}-api-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--%{version}.sql
%{__cp} -f %{sname}-packaging/target/classes/%{sname}--unpackaged.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql

%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.control %{buildroot}%{pginstdir}/share/extension

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT README.md
%else
%doc README.md
%license COPYRIGHT
%endif
%{pginstdir}/lib/libpljava-so-%{version}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}--1*.sql
%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql
%{pginstdir}/share/%{sname}/%{sname}-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-examples-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-api-%{version}.jar

%changelog
* Fri Jul 10 2020 * Devrim Gündüz <devrim@gunduz.org> - 1.5.5-1
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
