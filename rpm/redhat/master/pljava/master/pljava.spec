%global debug_package %{nil}
%global sname		pljava

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	1.5.1
Release:	b1_1%{?dist}.1
License:	BSD
Group:		Applications/Databases
URL:		http://tada.github.io/pljava/
Patch0:		%{sname}-pg%{pgmajorversion}-buildxml.patch

Source0:	https://github.com/tada/pljava/archive/V1_5_1b1.tar.gz
Source1:	%{sname}.pom

BuildRequires:	java-1.8.0-openjdk-devel, openssl-devel
Requires:	java-headless >= 1:1.8

%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -q -n pljava-1_5_1b1
%patch0 -p0

%build
export CLASSPATH=
mvn clean install

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/lib
%{__cp} -f %{sname}-so/target/nar/%{sname}-so-%{version}-BETA1-amd64-Linux-gpp-plugin/lib/amd64-Linux-gpp/plugin/libpljava-so-%{version}-BETA1.so %{buildroot}%{pginstdir}/lib

%{__install} -d %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}/target/%{sname}-%{version}-BETA1.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-api/target/%{sname}-api-%{version}-BETA1.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-packaging/target/classes/pljava.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--%{version}.sql
%{__cp} -f %{sname}-packaging/target/classes/pljava--unpackaged.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql

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
%{pginstdir}/lib/libpljava-so-%{version}-BETA1.so
%{pginstdir}/share/extension/pljava.control
%{pginstdir}/share/pljava/pljava--%{version}.sql
%{pginstdir}/share/pljava/pljava--unpackaged--%{version}.sql
%{pginstdir}/share/pljava/pljava-%{version}-BETA1.jar
%{pginstdir}/share/pljava/pljava-api-%{version}-BETA1.jar

%changelog
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
