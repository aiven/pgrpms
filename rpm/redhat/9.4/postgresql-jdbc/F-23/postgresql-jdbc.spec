%global section		devel
%global upstreamrel	1207
%global upstreamver	9.4.%{upstreamrel}
%global pgmajorversion	95
%global sname		postgresql-jdbc
%global tarballname	pgjdbc-REL%{upstreamver}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	%{upstreamver}
Release:	2%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
Group:		Applications/Databases
URL:		https://jdbc.postgresql.org/

Source0:	https://github.com/pgjdbc/pgjdbc/archive/REL%{version}.tar.gz
# originally http://repo2.maven.org/maven2/postgresql/postgresql/8.4-701.jdbc4/postgresql-8.4-701.jdbc4.pom:
Source1:	%{name}.pom

BuildArch:	noarch
BuildRequires:	java-1.8.0-openjdk-devel
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
%setup -c -q -n %{tarballname}

%{__mv} -f %{tarballname}/* .
%{__rm} -f %{tarballname}/.gitattributes
%{__rm} -f %{tarballname}/.gitignore
%{__rm} -f %{tarballname}/.travis.yml

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs %{__rm} -f

%build

export CLASSPATH=
# Ideally we would run "sh update-translations.sh" here, but that results
# in inserting the build timestamp into the generated messages_*.class
# files, which makes rpmdiff complain about multilib conflicts if the
# different platforms don't build in the same minute.  For now, rely on
# upstream to have updated the translations files before packaging.

mvn -DskipTests -P release-artifacts clean package

%install
%{__install} -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
%{__install} -m 644 pgjdbc/target/postgresql-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

pushd %{buildroot}%{_javadir}
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks.  (Probably only the jdbc3 symlink really makes sense?)
%{__ln_s} postgresql%{pgmajorversion}-jdbc.jar postgresql-jdbc2.jar
%{__ln_s} postgresql%{pgmajorversion}-jdbc.jar postgresql-jdbc2ee.jar
%{__ln_s} postgresql%{pgmajorversion}-jdbc.jar postgresql-jdbc3.jar
popd

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{version}/g' %{SOURCE1} >JPP-%{name}.pom
%{__install} -d -m 755 %{buildroot}%{_mavenpomdir}/
%{__install} -m 644 JPP-%{name}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

%{__install} -d -m 755 %{buildroot}%{_javadocdir}
%{__cp} -ra pgjdbc/target/apidocs %{buildroot}%{_javadocdir}/%{name}
%{__install} -d pgjdbc/target/apidocs docs/%{name}

%check
%if 0%{?runselftest}
# Note that this requires to have PostgreSQL properly configured;  for this
# reason the testsuite is turned off by default (see org/postgresql/test/README)
test_log=test.log
# TODO: more reliable testing
mvn clean package 2>&1 | tee test.log | grep FAILED
test $? -eq 0 && { cat test.log ; exit 1 ; }
%endif

%files -f .mfiles
%doc LICENSE README.md
%{_javadir}/%{sname}2.jar
%{_javadir}/%{sname}2ee.jar
%{_javadir}/%{sname}3.jar

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Wed Feb 10 2016 John Harvey <john.harvey@crunchydata.com> - 9.4.1207-2
- Fix broken links to jar files.
- Trim changelog (Devrim)

* Tue Jan 5 2016 John Harvey <john.harvey@crunchydata.com> - 9.4.1207-1
- Update to 9.4 build 1207 (maven support)
- Use some more macros, where appropriate (Devrim)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.1200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 04 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.1200-1
- rebase to most recent version (#1188827)
