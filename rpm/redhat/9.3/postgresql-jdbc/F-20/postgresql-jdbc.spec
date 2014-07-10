%global section		devel
%global upstreamver	9.3-1101
%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname postgresql-jdbc

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	9.3.1101
Release:	1%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:	http://jdbc.postgresql.org/download/%{sname}-%{upstreamver}.src.tar.gz
# originally http://repo2.maven.org/maven2/postgresql/postgresql/8.4-701.jdbc4/postgresql-8.4-701.jdbc4.pom:
Source1:	%{name}.pom

BuildArch:	noarch
BuildRequires:	java-1.7.0-openjdk-devel
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	junit
# gettext is only needed if we try to update translations
#BuildRequires:	gettext
Requires:	jpackage-utils
Requires:	java-headless >= 1:1.8

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
%setup -c -q -n postgresql-jdbc-9.3-1101.src/

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
install -m 644 jars/postgresql-%{upstreamver}.jdbc41.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar


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


%check
%if 0%{?runselftest}
# Note that this requires to have PostgreSQL properly configured;  for this
# reason the testsuite is turned off by default (see org/postgresql/test/README)
ant test 2>&1 | tee test.log | grep FAILED
test $? -eq 0 && { cat test.log ; exit 1 ; }
%endif


%files -f .mfiles
%doc LICENSE README.md doc/*
%{_javadir}/%{sname}2.jar
%{_javadir}/%{sname}2ee.jar
%{_javadir}/%{sname}3.jar

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Wed Jul 9 2014 Devrim Gunduz <devrim@gunduz.org> 0:9.3.1101-1PGDG
- Update to 9.3 build 1101
- Remove gcj support, now deprecated.
- Sync spec file Fedora rawhide.

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

