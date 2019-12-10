%global tarballname	pgjdbc-REL%{version}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	42.2.9
Release:	1%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
URL:		https://jdbc.postgresql.org/
Source0:	https://github.com/pgjdbc/pgjdbc/archive/REL%{version}.tar.gz
Source1:	%{name}.pom
BuildArch:	noarch

Requires:	jpackage-utils
Requires:	java-headless >= 1:1.8
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	java-1_8_0-openjdk-devel
%endif
%else
BuildRequires:	java-1.8.0-openjdk-devel
%endif

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

%if 0%{?rhel} && 0%{?rhel} == 7
%pom_remove_plugin :karaf-maven-plugin pgjdbc
%endif

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

%if 0%{?rhel} && 0%{?rhel} <= 6 || 0%{?suse_version} >= 1315
%files
%doc LICENSE README.md
%else
%files
%doc README.md
%license LICENSE
%{_javadir}/%{name}.jar
%endif
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_javadir}/%{name}.jar
%{_datadir}/maven2/poms/JPP-%{name}.pom
%endif
# ...and SLES locates .pom file somewhere else:
%if 0%{?suse_version} >= 1315
%{_javadir}/%{name}.jar
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?fedora}
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?fedora} && 0%{?fedora} <= 27
%{_datadir}/maven-metadata/%{name}.xml
%endif
%{_javadir}/postgresql-jdbc2.jar
%{_javadir}/postgresql-jdbc2ee.jar
%{_javadir}/postgresql-jdbc3.jar
%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.89-1
- Update to 42.2.9

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.8-1
- Update to 42.2.8

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.7-1.1
- Rebuild for PostgreSQL 12

* Wed Sep 11 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.7
- Update to 42.2.7

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.6-1
- Update to 42.2.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.5-1.1
- Rebuild against PostgreSQL 11.0

* Mon Aug 27 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.5-1
- Update to 42.2.5, which fixes CVE-2018-10936

* Sun Jul 15 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.4-1
- Update to 42.2.4

* Sat Mar 17 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.2-2
- Fix SLES builds

* Fri Mar 16 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.2-1
- Update to 42.2.2, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.2

* Sat Jan 27 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.1-1
- Update to 42.2.1, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.1

* Thu Jan 18 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.0-1
- Update to 42.2.0, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.0

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.4-1
- Update to 42.1.4, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.1.4

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.3-1
- Update to 42.1.3

* Thu Jul 13 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.2-1
- Update to 42.1.2

* Wed May 10 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.1-1
- Update to 42.1.1

* Mon Feb 20 2017 Devrim Gündüz <devrim@gunduz.org> - 42.0.0-1
- Update to 42.0.0

* Thu Nov 17 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1212-1
- Update to 9.4.1212

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
