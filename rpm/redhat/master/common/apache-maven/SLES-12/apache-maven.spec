%global profile_d_dir %{_sysconfdir}/profile.d
%global maven_name maven
%global maven_confdir %{_sysconfdir}/%{maven_name}
%global prj_datadir %{_datadir}/%{name}
%global java_ver_min 1.8.0

Name:           apache-maven
Version:        3.3.9
Release:        4%{?dist}
Summary:        Java project management and project comprehension tool binary
Epoch:          0

Group:          Development/Tools
License:        ASL 2.0 and MIT and BSD
URL:            http://maven.apache.org/

Source0:        http://apache.cs.utah.edu/maven/maven-3/%{version}/binaries/%{name}-%{version}-bin.tar.gz
Source1:        bash_completion.d-%{name}
Source15:       %{name}-jpp-script

BuildArch: noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if "%{?el6}"
BuildRequires: java-%{java_ver_min}-openjdk-devel
%else
BuildRequires: java-devel >= %{java_ver_min}
%endif
BuildRequires:  jpackage-utils
BuildRequires:  grep

# maven 3 Requires JDK, see http://maven.apache.org/download.cgi
Requires:  java >= %{java_ver_min}
%if "%{?el6}"
Requires: java-%{java_ver_min}-openjdk-devel
%else
Requires: java-devel >= %{java_ver_min}
%endif
Requires:  jpackage-utils

# For those who need maven, but don't want or cannot install maven2 for Fedora.
# RHEL-6, for example, by default do not have maven.
Provides:  maven2 = %{version}-%{release}

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

Note that this package is binary version, thus cannot go in official
Fedora repo.

%prep
%setup -q
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i 's/\r//' NOTICE
%{__sed} -i 's/\r//' README.txt

%clean
%__rm -rf $RPM_BUILD_ROOT

%build

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
%__install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/maven

%__mkdir -p $RPM_BUILD_ROOT%{_bindir}
%__mkdir -p $RPM_BUILD_ROOT%{prj_datadir}/bin
%__install -pm 644 bin/m2.conf $RPM_BUILD_ROOT%{_sysconfdir}/
ln -sf %{_sysconfdir}/m2.conf $RPM_BUILD_ROOT%{prj_datadir}/bin
%__install -pm 755 bin/mvn $RPM_BUILD_ROOT%{prj_datadir}/bin
ln -sf %{prj_datadir}/bin/mvn $RPM_BUILD_ROOT%{_bindir}/
%__install -pm 755 bin/mvnDebug $RPM_BUILD_ROOT%{prj_datadir}/bin
ln -sf %{prj_datadir}/bin/mvnDebug $RPM_BUILD_ROOT%{_bindir}/
%__install -pm 755 %{SOURCE15} $RPM_BUILD_ROOT%{prj_datadir}/bin/mvn-jpp
%__install -pm 755 bin/mvnyjp  $RPM_BUILD_ROOT%{prj_datadir}/bin
ln -sf %{prj_datadir}/bin/mvnyjp $RPM_BUILD_ROOT%{_bindir}/

%__mkdir -p $RPM_BUILD_ROOT%{maven_confdir}
%__cp -R conf/* $RPM_BUILD_ROOT%{maven_confdir}
ln -sf %{maven_confdir} $RPM_BUILD_ROOT%{prj_datadir}/conf

%__cp -R boot $RPM_BUILD_ROOT/%{prj_datadir}

## jar files
%__mkdir -p $RPM_BUILD_ROOT/%{prj_datadir}/lib
%__mkdir -p $RPM_BUILD_ROOT/%{prj_javadir}
%__mkdir -p $RPM_BUILD_ROOT/%{_javadir}/aether
%__mkdir -p $RPM_BUILD_ROOT/%{_javadir}/%{maven_name}
%__mkdir -p $RPM_BUILD_ROOT/%{_javadir}/maven-wagon
%__mkdir -p $RPM_BUILD_ROOT/%{_javadir}/plexus
%__mkdir -p $RPM_BUILD_ROOT/%{_javadir}/sisu
pushd lib
for f in * ;do
  if [[ -d "$f" ]];then
    cp -R "$f" $RPM_BUILD_ROOT/%{prj_datadir}/lib
  elif [[ "$f" =~ \.jar$ ]];then
      deVersioned=
      if [[ "$f" =~ -([0-9.M]+)\.jar$ ]];then
        deVersioned=`echo $f | sed -e "s/-${BASH_REMATCH[1]}//"`
      else
        deVersioned=$f
      fi
      case $f in
        aether* )
          destJar=$RPM_BUILD_ROOT%{_javadir}/aether/$deVersioned
          ;;
        wagon-* )
          deModule=`echo $deVersioned | sed -e 's/wagon-//'`
          destJar=$RPM_BUILD_ROOT%{_javadir}/maven-wagon/$deModule
          ;;
        maven-* )
          destJar=$RPM_BUILD_ROOT%{_javadir}/%{maven_name}/$deVersioned
          ;;
        plexus-* )
          deModule=`echo $deVersioned | sed -e 's/plexus_//'`
          destJar=$RPM_BUILD_ROOT%{_javadir}/plexus/$deModule
          ;;
        org.eclipse.sisu.* )
          deModule=`echo $deVersioned | sed -e 's/org.eclipse.sisu./sisu-/'`
          destJar=$RPM_BUILD_ROOT%{_javadir}/sisu/$deModule
          ;;
        * )  
          destJar=$RPM_BUILD_ROOT%{_javadir}/$deVersion
          ;;
      esac
      install -pm 644 "$f" $RPM_BUILD_ROOT%{prj_datadir}/lib
      ln -sf %{prj_datadir}/lib/$f $destJar
  else
      install -pm 644 "$f" $RPM_BUILD_ROOT%{prj_datadir}/lib
  fi
done
popd

%__mkdir -p $RPM_BUILD_ROOT%{profile_d_dir}
%__cat >>$RPM_BUILD_ROOT%{profile_d_dir}/apache-maven.sh <<EOF
MAVEN_HOME=%{prj_datadir}
M2_HOME=\$MAVEN_HOME
export MAVEN_HOME
export M2_HOME
EOF

%__cat >>$RPM_BUILD_ROOT%{profile_d_dir}/apache-maven.csh <<EOF
setenv MAVEN_HOME %{prj_datadir}
setenv M2_HOME \$MAVEN_HOME
EOF

%files
%defattr(-,root,root,-)
%doc LICENSE  NOTICE  README.txt
%{_bindir}/m*
%{_javadir}/aether/*.jar
%{_javadir}/%{maven_name}
%{_javadir}/maven-wagon/*.jar
%{_javadir}/plexus/*.jar
%{_javadir}/sisu/*.jar
%{_javadir}/*.jar
%{prj_datadir}
%config %{profile_d_dir}/apache-maven.*sh
%config(noreplace) %{_sysconfdir}/m2.conf
%config(noreplace) %{_sysconfdir}/%{maven_name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{maven_name}

%changelog
* Tue Jan 5 2016 Devrim Gündüz <devrim @gunduz.org> - 0:3.3.9-4
- Update to 3.3.9

* Wed Oct 21 2015 Ding-Yi Chen <dchen at redhat.com> - 0:3.3.3-4
- CentOS 6 only has java-<ver>-openjdk-devel, but not java-devel-<ver>

* Mon Oct 19 2015 Ding-Yi Chen <dchen at redhat.com> - 0:3.3.3-3
- Remove Epoch on JDK dependencies.

* Wed Oct 14 2015 Ding-Yi Chen <dchen at redhat.com> - 0:3.3.3-2
- Version 3.3.3 require Java 1.7

* Thu Oct 08 2015 Ding-Yi Chen <dchen at redhat.com> - 0:3.3.3-1
- Upstream update to 3.3.3

* Mon Jan 19 2015 Ding-Yi Chen <dchen at redhat.com> - 0:3.2.5-1
- Upstream update to 3.2.5

* Tue Nov 25 2014 Ding-Yi Chen <dchen at redhat.com> - 0:3.2.3-1
- Upstream update to 3.2.3
- Change the mirror URL.

* Mon Jun 16 2014 Ding-Yi Chen <dchen at redhat.com> - 0:3.2.1-2
- Setting files are set with (noreplace)
- The file structure is now looks like maven in RHEL7
- Executables are available in /usr/bin
- /usr/share/apache-maven/conf is now a link to /etc/maven.
  So rpm -Uvh might not work, please remove the previous apache-maven
  before install this version.

* Tue Mar 04 2014 Ding-Yi Chen <dchen at redhat.com> - 0:3.2.1-1
- Upstream update to 3.2.1
- Fixed java.io.FileNotFoundException: /usr/share/apache-maven/conf/logging


* Thu Feb 13 2014 Ding-Yi Chen <dchen at redhat.com> - 0:3.1.1-1
- Upstream update to 3.1.1

* Wed Aug 3 2011 Ding-Yi Chen <dchen at redhat.com> - 0:3.0.3-1
- Upstream update to 3.0.3

* Thu Dec 9 2010 Sean Flanigan <sflaniga at redhat dot com> - 0:3.0-4
- Removed broken .jar links

* Fri Dec 3 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:3.0-3
- Added: provide maven2, For those who need maven, but don't want or
  cannot install maven2 for Fedora.


* Fri Nov 26 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:3.0-2
- Now requires java-devel instead of java, as mvn seems require javac
  to work properly.

* Tue Oct 12 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:3.0-1
- Update to Maven3.

* Thu Jul 08 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-7
- Don't tried to replace the whole Fedora's maven2, but cooperate with it.
  but still insert itself before Fedora's maven2.

* Thu Apr 01 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-6
-Correct the apache-maven.csh

* Wed Mar 31 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-5
-Correct the maven-plugins version.

* Mon Mar 29 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-4
-Add Epoch
-Add plugins

* Tue Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-3
Fixed profile.d scripts

* Tue Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-2
Modify conflicts

* Tue Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-1
- Initial package.

