%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname	pgagent

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%global _varrundir %{_localstatedir}/run/%{name}

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.4.0
Release:	4%{?dist}
License:	PostgreSQL
Source0:	https://download.postgresql.org/pub/pgadmin3/release/%{sname}/pgAgent-%{version}-Source.tar.gz
Source2:	%{sname}-%{pgmajorversion}.service
Source3:	%{sname}.init
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql%{pgmajorversion}-devel cmake

%if %{systemd_enabled}
BuildRequires:		systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
# This is for older spec files (RHEL <= 6)
Group:			Applications/Databases
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%description
pgAgent is a job scheduler for PostgreSQL which may be managed
using pgAdmin.

%pre
if [ $1 -eq 1 ] ; then
groupadd -r pgagent >/dev/null 2>&1 || :
useradd -g pgagent -r -s /bin/false \
	-c "pgAgent Job Schedule" pgagent >/dev/null 2>&1 || :
touch /var/log/pgagent_%{pgmajorversion}.log
fi
%{__chown} pgagent:pgagent /var/log/pgagent_%{pgmajorversion}.log
%{__chmod} 0700 /var/log/pgagent_%{pgmajorversion}.log

%prep
%setup -q -n pgAgent-%{version}-Source

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D PG_CONFIG_PATH:FILEPATH=/%{pginstdir}/bin/pg_config -D STATIC_BUILD:BOOL=OFF .

%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Rename pgagent binary, so that we can have parallel installations:
%{__mv} -f %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}
# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

%if %{systemd_enabled}
# Install unit file
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}_%{pgmajorversion}.service
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 root root -
EOF
%else
# install init script
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE2} %{buildroot}/%{_initrddir}/%{name}
%endif

%post
if [ $1 -eq 1 ] ; then
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%tmpfiles_create
    # Initial installation
%else
chkconfig --add %{name}
%endif
fi

%preun
%if %{systemd_enabled}
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi
%else
	chkconfig --del %{name}
%endif

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if %{systemd_enabled}
%doc README
%license LICENSE
%else
%doc README LICENSE
%endif
%{_bindir}/%{name}
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%if %{systemd_enabled}
%ghost %{_varrundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}_%{pgmajorversion}.service
%else
%{_initrddir}/%{name}
%endif
%{pginstdir}/share/extension/%{sname}--3.4.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--3.4.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Oct 19 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-4
- Fix PostgreSQL version in unit file and init script. Per
  report from Alf Normann Klausen, pgsql bug #14370.

* Fri Jan 22 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-3
- Create unified spec file that works with all distros.
- Fix an issue with user and group creation.

* Wed Dec 30 2015 Devrim GUNDUZ <devrim@gunduz.org> 3.4.0-2
- Build with -fPIC, per Fedora 23+ guidelines.
- Use more macros.
- Update license.
- Update download URL.

* Fri Oct 17 2014 Devrim GUNDUZ <devrim@gunduz.org> 3.4.0-1
- Update to 3.4.0
- Use macros for pgagent, where appropriate.
- Switch to systemd, and use unit file instead of sysV init
  script.
- Add PostgreSQL major version number to pgagent binary, to
  enable parallel installations.

* Mon Sep 17 2012 Devrim GUNDUZ <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Wed Sep 12 2012 Devrim GUNDUZ <devrim@gunduz.org> 3.2.1-1
- Various updates from David Wheeler
- Update to 3.2.1
- Improve init script

* Tue Dec 6 2011 Devrim GUNDUZ <devrim@gunduz.org> 3.0.1-1
- Initial packaging

