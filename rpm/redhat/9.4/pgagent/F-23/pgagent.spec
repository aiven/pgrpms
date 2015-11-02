%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname	pgagent

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.4.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source:		http://ftp.postgresql.org/pub/pgadmin3/release/%{sname}/pgAgent-%{version}-Source.tar.gz
Source2:	%{sname}-%{pgmajorversion}.service
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql%{pgmajorversion}-devel cmake

%description
pgAgent is a job scheduler for PostgreSQL which may be managed
using pgAdmin. Prior to pgAdmin v1.9, pgAgent shipped as part 
of pgAdmin. From pgAdmin v1.9 onwards, pgAgent is shipped as 
a separate application.

%pre
groupadd -o -r pgagent >/dev/null 2>&1 || :
useradd -o -g pgagent -r -s /bin/false \
	-c "pgAgent Job Schedule" pgagent >/dev/null 2>&1 || :
touch /var/log/pgagent_%{pgmajorversion}.log
chown pgagent:pgagent /var/log/pgagent_%{pgmajorversion}.log
chmod 0700 /var/log/pgagent_%{pgmajorversion}.log

%prep
%setup -q -n pgAgent-%{version}-Source

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D PG_CONFIG_PATH:FILEPATH=/%{pginstdir}/bin/pg_config -D STATIC_BUILD:BOOL=OFF .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Install unit file
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}_%{pgmajorversion}.service

# Rename pgagent binary, so that we can have parallel installations:
%{__mv} -f %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}

# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
        # Package removal, not upgrade
        /bin/systemctl --no-reload disable %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
        /bin/systemctl stop %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
        # Package upgrade, not uninstall
        /bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%{_unitdir}/%{sname}_%{pgmajorversion}.service
%{pginstdir}/share/extension/%{sname}--3.4.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--3.4.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
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

