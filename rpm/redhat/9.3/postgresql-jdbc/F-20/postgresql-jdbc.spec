# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz
# Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%global section		devel
%{!?upstreamver:%global upstreamver     9.3-1100}
%global pgmajorversion 93
%global sname postgresql-jdbc

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	9.3.1100
Release:	2PGDG%{?dist}

# ASL 2.0 applies only to postgresql93-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:        http://jdbc.postgresql.org/download/%{sname}-%{upstreamver}.src.tar.gz

# originally http://repo2.maven.org/maven2/postgresql/postgresql/8.4-701.jdbc4/postgresql-8.4-701.jdbc4.pom:
Source1:	%{name}.pom

BuildArch:	noarch
BuildRequires:	java-devel
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	junit
# gettext is only needed if we try to update translations
#BuildRequires:	gettext
Requires:	java
Requires:	jpackage-utils

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%package javadoc
Summary:        API docs for %{name}
Group:          Documentation

%description javadoc
This package contains the API Documentation for %{name}.

%prep
%setup -c -q
mv -f %{sname}-%{upstreamver}.src/* .
rm -f %{sname}-%{upstreamver}.src/.gitignore
rmdir %{sname}-%{upstreamver}.src

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

ant jar publicapi

%install
install -d $RPM_BUILD_ROOT%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar $RPM_BUILD_ROOT%{_javadir}/%{sname}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks.  (Probably only the jdbc3 symlink really makes sense?)
ln -s postgresql-jdbc.jar postgresql-jdbc2.jar
ln -s postgresql-jdbc.jar postgresql-jdbc2ee.jar
ln -s postgresql-jdbc.jar postgresql-jdbc3.jar
popd

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{upstreamver}/g' %{SOURCE1} >JPP-%{name}.pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}/
install -m 644 JPP-%{name}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -ra build/publicapi $RPM_BUILD_ROOT%{_javadocdir}/%{name}
install -d build/publicapi docs/%{name}

%files -f .mfiles
%doc LICENSE doc/*
%{_javadir}/%{name}2.jar
%{_javadir}/%{name}2ee.jar
%{_javadir}/%{name}3.jar

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Thu Dec 12 2013 Devrim Gunduz <devrim@gunduz.org> 0:9.3.1100-2PGDG
- add javadoc subpackage
- don't use removed macro %%add_to_maven_depmap (#992816)
- lint: trim-lines, reuse %%{name} macro, fedora-review fixes
- merge cleanup changes by Stano Ochotnicky

* Tue Nov 05 2013 Devrim Gunduz <devrim@gunduz.org> 0:9.3.1100-1PGDG
- Update to 9.3 build 1100

* Mon Jan 14 2013 Devrim Gunduz <devrim@gunduz.org> 0:9.2.1002-1PGDG
- Update to 9.2 build 1002

* Wed Oct 3 2012 Devrim Gunduz <devrim@gunduz.org> 0:9.2.1000-1PGDG
- Update to 9.2 build 1000

* Mon Sep 12 2011 Devrim Gunduz <devrim@gunduz.org> 0:9.1.901-1PGDG
- Update to 9.1 build 901

* Tue Sep 21 2010 Devrim Gunduz <devrim@gunduz.org> 0:9.0.801-1PGDG
- Initial packaging of build 801, for PostgreSQL 9.0
- Trim changelog
