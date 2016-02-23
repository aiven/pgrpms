%global pgmajorversion	95
%global sname		pljava

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	1.5.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://tada.github.io/pljava/
Patch0:		pljava-makefile.patch

Source0:	https://github.com/tada/pljava/archive/V1_5_0b2.tar.gz
Source1:	%{name}.pom

BuildArch:	noarch
BuildRequires:	java-1.8.0-openjdk-devel
Requires:	java-headless >= 1:1.8

%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -c -q
%patch0 -p0

%{__mv} -f pljava-1_5_0b2/* .

%build
export CLASSPATH=
mvn clean install

%install
install -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 ./%{sname}-packaging/target/%{sname}-pg9.5-amd64-Linux-gpp.jar %{buildroot}%{_javadir}/%{name}.jar

%files
%doc COPYRIGHT README.md
%{_javadir}/%{name}.jar

%changelog
* Tue Feb 23 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0beta2-1
- Initial packaging for PostgreSQL RPM repository
