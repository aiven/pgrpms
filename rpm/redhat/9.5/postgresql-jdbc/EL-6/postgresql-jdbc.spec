%global section		devel
%global upstreamrel	1207
%global upstreamver	9.4.%{upstreamrel}
%global pgmajorversion	94
%global sname		postgresql-jdbc
%global tarballname	pgjdbc-REL%{upstreamver}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	%{upstreamver}
Release:	1%{?dist}
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
install -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 pgjdbc/target/postgresql-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

pushd %{buildroot}%{_javadir}
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks.  (Probably only the jdbc3 symlink really makes sense?)
%{__ln_s} postgresql-jdbc.jar postgresql-jdbc2.jar
%{__ln_s} postgresql-jdbc.jar postgresql-jdbc2ee.jar
%{__ln_s} postgresql-jdbc.jar postgresql-jdbc3.jar
popd

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{version}/g' %{SOURCE1} >JPP-%{name}.pom
install -d -m 755 %{buildroot}%{_mavenpomdir}/
install -m 644 JPP-%{name}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

install -d -m 755 %{buildroot}%{_javadocdir}
%{__cp} -ra pgjdbc/target/apidocs %{buildroot}%{_javadocdir}/%{name}
install -d pgjdbc/target/apidocs docs/%{name}

%check
%if 0%{?runselftest}
# Note that this requires to have PostgreSQL properly configured;  for this
# reason the testsuite is turned off by default (see org/postgresql/test/README)
test_log=test.log
# TODO: more reliable testing
mvn clean package 2>&1 | tee test.log | grep FAILED
test $? -eq 0 && { cat test.log ; exit 1 ; }
%endif

%files
%{_javadir}/%{sname}2.jar
%{_javadir}/%{sname}2ee.jar
%{_javadir}/%{sname}3.jar

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Tue Jan 5 2016 John Harvey <john.harvey@crunchydata.com> - 9.4.1207-1
- Update to 9.4 build 1207 (maven support)
- Use some more macros, where appropriate (Devrim)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.1200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 04 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.1200-1
- rebase to most recent version (#1188827)

* Mon Jul 14 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.1102-1
- Rebase to most recent version (#1118667)
- revert back upstream commit for travis build

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.1101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.1101-3
- run upstream testsuite when '%%runselftest' defined

* Wed Apr 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.1101-2
- Add explicit requires on java-headless

* Wed Apr 23 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.1101-1
- Rebase to most recent version (#1090366)

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 9.2.1002-5
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 06 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.1002-4
- add javadoc subpackage

* Tue Aug 06 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.1002-4
- don't use removed macro %%add_to_maven_depmap (#992816)
- lint: trim-lines, reuse %%{name} macro, fedora-review fixes
- merge cleanup changes by Stano Ochotnicky

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.1002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.1002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Tom Lane <tgl@redhat.com> 9.2.1002-1
- Update to build 9.2-1002 (just to correct mispackaging of source tarball)

* Tue Nov 13 2012 Tom Lane <tgl@redhat.com> 9.2.1001-1
- Update to build 9.2-1001 for compatibility with PostgreSQL 9.2

* Sun Jul 22 2012 Tom Lane <tgl@redhat.com> 9.1.902-1
- Update to build 9.1-902

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.901-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Tom Lane <tgl@redhat.com> 9.1.901-3
- Change BuildRequires: java-1.6.0-openjdk-devel to just java-devel.
  As of 9.1-901, upstream has support for JDBC4.1, so we don't have to
  restrict to JDK6 anymore, and Fedora is moving to JDK7
Resolves: #796580

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.901-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Tom Lane <tgl@redhat.com> 9.1.901-1
- Update to build 9.1-901 for compatibility with PostgreSQL 9.1

* Mon Aug 15 2011 Tom Lane <tgl@redhat.com> 9.0.801-4
- Add BuildRequires: java-1.6.0-openjdk-devel to ensure we have recent JDK
Related: #730588
- Remove long-obsolete minimum versions from BuildRequires

* Sun Jul 17 2011 Tom Lane <tgl@redhat.com> 9.0.801-3
- Switch to non-GCJ build, since GCJ is now deprecated in Fedora
Resolves: #722247
- Use %%{_mavendepmapfragdir} to fix FTBFS with maven 3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 9.0.801-1
- Update to build 9.0-801

* Mon May 31 2010 Tom Lane <tgl@redhat.com> 8.4.701-4
- Update gcj_support sections to meet Packaging/GCJGuidelines;
  fixes FTBFS in F-14 rawhide

* Tue Nov 24 2009 Tom Lane <tgl@redhat.com> 8.4.701-3
- Seems the .pom file *must* have a package version number in it, sigh
Resolves: #538487

* Mon Nov 23 2009 Tom Lane <tgl@redhat.com> 8.4.701-2
- Add a .pom file to ease use by maven-based packages (courtesy Deepak Bhole)
Resolves: #538487

* Tue Aug 18 2009 Tom Lane <tgl@redhat.com> 8.4.701-1
- Update to build 8.4-701

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:8.3.603-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Tom Lane <tgl@redhat.com> 8.3.603-3
- Avoid multilib conflict caused by overeager attempt to rebuild translations

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:8.3.603-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 8.3.603-1.1
- drop repotag

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 8.3.603-1jpp
- Update to build 8.3-603

* Sun Aug 12 2007 Tom Lane <tgl@redhat.com> 8.2.506-1jpp
- Update to build 8.2-506

* Tue Apr 24 2007 Tom Lane <tgl@redhat.com> 8.2.505-1jpp
- Update to build 8.2-505
- Work around 1.4 vs 1.5 versioning inconsistency

* Fri Dec 15 2006 Tom Lane <tgl@redhat.com> 8.2.504-1jpp
- Update to build 8.2-504

* Wed Aug 16 2006 Tom Lane <tgl@redhat.com> 8.1.407-1jpp.4
- Fix Requires: for rebuild-gcj-db (bz #202544)

* Wed Aug 16 2006 Fernando Nasser <fnasser@redhat.com> 8.1.407-1jpp.3
- Merge with upstream

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> 8.1.407-1jpp.2
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:8.1.407-1jpp.1
- rebuild

* Wed Jun 14 2006 Tom Lane <tgl@redhat.com> 8.1.407-1jpp
- Update to build 8.1-407

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 8.1.405-2jpp
- Back-patch upstream fix to support unspecified-type strings.

* Thu Feb 16 2006 Tom Lane <tgl@redhat.com> 8.1.405-1jpp
- Split postgresql-jdbc into its own SRPM (at last).
- Build it from source.  Add support for gcj compilation.
