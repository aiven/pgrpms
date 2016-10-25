%global tarballname	pgjdbc-REL%{version}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	9.4.1211
Release:	1%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
Group:		Applications/Databases
URL:		https://jdbc.postgresql.org/
Source0:	https://github.com/pgjdbc/pgjdbc/archive/REL%{version}.tar.gz
Source1:	%{name}.pom
BuildArch:	noarch

Requires:	jpackage-utils
Requires:	java-headless >= 1:1.8
BuildRequires:	java-1.8.0-openjdk-devel

%if 0%{?rhel} && 0%{?rhel} <= 6
# On RHEL 6, we depend on the apache-maven package that we provide via our
# repo. Build servers should not have any other apache-maven package from other
# repos, because they depend on java-1.7.0, which is not supported by pgjdbc.
# Please note that we don't support RHEL 5 for this package. RHEL 7 already
# includes apache-maven package in its own repo.
BuildRequires:	apache-maven >= 3.0.0
%else
# On the remaining distros, use the maven package supplied by OS.
BuildRequires:	maven
%endif

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%package javadoc
Summary:	API docs for %{name}
Group:		Documentation

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
%{__ln_s} %{name}.jar postgresql-jdbc2.jar
%{__ln_s} %{name}.jar postgresql-jdbc2ee.jar
%{__ln_s} %{name}.jar postgresql-jdbc3.jar
popd

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{version}/g' %{SOURCE1} >JPP-%{name}.pom
%{__install} -d -m 755 %{buildroot}%{_mavenpomdir}/
%{__install} -m 644 JPP-%{name}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%if 0%{?rhel} && 0%{?rhel} <= 6
:
%else
%add_maven_depmap
%endif

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

%if 0%{?rhel} && 0%{?rhel} <= 6
%files
%doc LICENSE README.md
%else
%files -f .mfiles
%doc README.md
%license LICENSE
%endif
%if 0%{?rhel} && 0%{?rhel} <= 6
# These files are installed with the other distros, but we don't need to list
# them on newer ones, as they are picked up by .mfiles above.
%{_javadir}/%{name}.jar
%{_datadir}/maven2/poms/JPP-%{name}.pom
%endif
%{_javadir}/postgresql-jdbc2.jar
%{_javadir}/postgresql-jdbc2ee.jar
%{_javadir}/postgresql-jdbc3.jar
%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Mon Sep 19 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1211-1
- Update to 9.4.1211

* Tue Mar 15 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1208-1
- Update to 9.4.1208, per #1034.
- Use more macros, per John Harvey. Closes #1017.

* Wed Feb 10 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1207-3
- Remove pgmajorversion from spec file, because this package does not
  depend on PostgreSQL version.
- Add more conditionals for unified spec file.
- Remove some BRs, per John Harvey.
- Specify maven version, per John Harvey.

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
