# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz
# Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%global _gcj_support 0
%global gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname postgresql-jdbc
%global section		devel
%global upstreamver	9.1-903

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	9.1.903
Release:	1%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:	http://jdbc.postgresql.org/download/%{sname}-%{upstreamver}.src.tar.gz
# originally http://repo2.maven.org/maven2/postgresql/postgresql/8.4-701.jdbc4/postgresql-8.4-701.jdbc4.pom:
Source1:	postgresql-jdbc.pom

%if ! %{gcj_support}
BuildArch:	noarch
%endif
# We require Java 1.6 because we support JDBC 4.0, not 4.1
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	junit
BuildRequires:	findutils
# gettext is only needed if we try to update translations
#BuildRequires:	gettext
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 1.0.31
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%endif
Requires:	java
Requires(post):	jpackage-utils
Requires(postun): jpackage-utils

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%prep
%setup -c -q
mv -f %{sname}-%{upstreamver}.src/* .
rm -f %{sname}-%{upstreamver}.src/.cvsignore
rm -rf %{sname}-%{upstreamver}.src

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs rm -f

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=

# Ideally we would run "sh update-translations.sh" here, but that results
# in inserting the build timestamp into the generated messages_*.class
# files, which makes rpmdiff complain about multilib conflicts if the
# different platforms don't build in the same minute.  For now, rely on
# upstream to have updated the translations files before packaging.

ant

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
# We are breaking  backwards compatibility here, and not adding symlinks anymore.
popd

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{upstreamver}/g' %{SOURCE1} >JPP-postgresql%{pgmajorversion}-jdbc.pom
install -d -m 755 %{buildroot}%{_mavenpomdir}/
install -m 644 JPP-postgresql%{pgmajorversion}-jdbc.pom %{buildroot}%{_mavenpomdir}/JPP-postgresql%{pgmajorversion}-jdbc.pom
%add_to_maven_depmap postgresql%{pgmajorversion} postgresql%{pgmajorversion} %{version} JPP postgresql%{pgmajorversion}-jdbc

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%files
%defattr(-,root,root)
%doc LICENSE README doc/*
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-postgresql%{pgmajorversion}-jdbc.pom

%changelog
* Mon Jan 14 2013 Devrim Gunduz <devrim@gunduz.org> 0:9.1.903-1PGDG
- Update to 9.1 build 903

* Thu Jul 5 2012 Devrim Gunduz <devrim@gunduz.org> 0:9.1.902-1PGDG
- Update to 9.1 build 902

* Mon Sep 12 2011 Devrim Gunduz <devrim@gunduz.org> 0:9.1.901-1PGDG
- Update to 9.1 build 901
- Apply major spec file changes from Fedora rawhide.:
 * Add BuildRequires: java-1.6.0-openjdk-devel to ensure we have recent JDK
   Related: #730588
 * Remove long-obsolete minimum versions from BuildRequires
 * Switch to non-GCJ build, since GCJ is now deprecated in Fedora
 * Use %%{_mavendepmapfragdir} to fix FTBFS with maven 3
 * Update gcj_support sections to meet Packaging/GCJGuidelines;
 * Add a .pom file to ease use by maven-based packages (courtesy Deepak Bhole)
   Resolves: #538487
- Comment cleanup.

* Tue Sep 21 2010 Devrim Gunduz <devrim@gunduz.org> 0:9.0.801-1PGDG
- Initial packaging of build 801, for PostgreSQL 9.0
- Trim changelog

