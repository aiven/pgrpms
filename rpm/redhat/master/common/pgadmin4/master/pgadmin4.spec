%global debug_package %{nil}
%global	pgadmin4instdir /usr/%{name}

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python3_sitelib}
%global PYTHON_SITELIB64 %{python3_sitelib64}

Name:		pgadmin4
Version:	4.24
Release:	1%{?dist}
Summary:	Management tool for PostgreSQL
License:	PostgreSQL
URL:		https://www.pgadmin.org
Source0:	https://download.postgresql.org/pub/pgadmin/%{name}/v%{version}/source/%{name}-%{version}.tar.gz
Source1:	https://download.postgresql.org/pub/pgadmin/%{name}/v%{version}/docs/%{name}-%{version}-docs.tar.gz
Source2:	%{name}.conf
Source3:	%{name}.tmpfiles.d
Source4:	%{name}.desktop.in
Source6:	%{name}.qt.conf.in
Source7:	%{name}-web-setup.sh
Source8:	%{name}.service.in

BuildRequires:	gcc-c++

Requires:	%{name}-web

%if 0%{?fedora} && 0%{?fedora} >= 30
BuildRequires:	%{name}-python3-flask-migrate >= 2.4.0 %{name}-python3-passlib >= 1.7.2
BuildRequires:	%{name}-python3-flask-security-too >= 3.3.3
BuildRequires:	python3-flask-principal >= 0.4.0
BuildRequires:	python3-dateutil >= 2.8.0 python3-simplejson >= 3.16.0
BuildRequires:	python3-flask-mail >= 0.9.1 python3-flask-gravatar >= 0.5.0
BuildRequires:	python3-flask-wtf >= 0.14.2 python3-flask >= 1.0.2
BuildRequires:	python3-flask-paranoid >= 0.2.0 python3-flask-login >= 0.4.1
BuildRequires:	python3-sqlalchemy >= 1.2.18 qt5-qtbase-devel >= 5.1 python3-devel
BuildRequires:	python3-blinker >= 1.4 python3-flask-sqlalchemy >= 2.3.2 python3-ldap3 >= 2.5.1
Requires:	%{name}-python3-flask-compress >= 1.4.0
Requires:	python3-babel python3-flask-babelex python3
Requires:	python3-alembic python3-mako python3-ldap3 >= 2.5.1
%global QMAKE	/usr/bin/qmake-qt5
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	%{name}-python3-flask >= 1.0.2
BuildRequires:	%{name}-python3-flask-security-too >= 3.3.3 %{name}-python3-flask-principal >= 0.4.0
BuildRequires:	%{name}-python3-flask-login >= 0.4.1 %{name}-python3-simplejson >= 3.16.0
BuildRequires:	%{name}-python3-blinker >= 1.4 %{name}-python3-flask-wtf >= 0.14.2
BuildRequires:	%{name}-python3-flask-sqlalchemy >= 2.3.2 %{name}-python3-Flask-Mail >= 0.9.1
BuildRequires:	%{name}-python3-dateutil >= 2.8.0 %{name}-python3-flask-gravatar
BuildRequires:	%{name}-python3-flask-paranoid >= 0.2
BuildRequires:	%{name}-python3-passlib >= 1.7.2
BuildRequires:	%{name}-python3-wtforms >= 2.2.1 %{name}-python3-flask-compress >= 1.4.0
BuildRequires:	python3-devel mesa-libGL-devel qt5-qtbase-devel >= 5.9.7 python36-ldap3 >= 2.5.1
Requires:	%{name}-python3-flask-babelex %{name}-python3-flask-compress >= 1.4.0
Requires:	%{name}-python3-sqlalchemy >= 1.2.18 %{name}-python3-babel
Requires:	%{name}-python3-mako %{name}-python3-alembic
Requires:	python36-ldap3 >= 2.5.1
%global QMAKE	/usr/bin/qmake-qt5
%endif

%if 0%{?rhel} && 0%{?rhel} == 8
BuildRequires:	%{name}-python3-passlib >= 1.7.2 %{name}-python3-dateutil >= 2.8.0 %{name}-python3-simplejson >= 3.16.0
BuildRequires:	%{name}-python3-Flask-Mail >= 0.9.1 %{name}-python3-flask-gravatar >= 0.5.0
BuildRequires:	%{name}-python3-flask-sqlalchemy >= 2.3.2 %{name}-python3-sqlalchemy >= 1.2.18
BuildRequires:	%{name}-python3-flask-security-too >= 3.3.3 %{name}-python3-flask-principal >= 0.4.0
BuildRequires:	%{name}-python3-flask-wtf >= 0.14.2 %{name}-python3-flask >= 1.0.2
BuildRequires:	%{name}-python3-flask-paranoid >= 0.2 %{name}-python3-flask-login >= 0.4.1
BuildRequires:	qt5-qtbase-devel >= 5.1 python3-devel python3-blinker >= 1.4 python3-ldap3 >= 2.5.1
Requires:	%{name}-python3-alembic %{name}-python3-flask-babelex
Requires:	%{name}-python3-flask-compress >= 1.4.0
Requires:	python3-mako python3 python3-babel python3-ldap3 >= 2.5.1
%global QMAKE	/usr/bin/qmake-qt5
%endif

%description
pgAdmin 4 is a rewrite of the popular pgAdmin3 management tool for the
PostgreSQL (http://www.postgresql.org) database.

pgAdmin 4 is written as a web application in Python, using jQuery and
Bootstrap for the client side processing and UI. On the server side,
Flask is being utilised.

Although developed using web technologies, we intend for pgAdmin 4 to
be usable either on a web server using a browser, or standalone on a
workstation. The runtime/ subdirectory contains a QT based runtime
application intended to allow this - it is essentially a browser and
Python interpretor in one package which will be capable of hosting the
Python application and presenting it to the user as a desktop
application.

%package	-n %{name}-web
Summary:	pgAdmin4 web package
Requires:	%{name}-docs
Requires:	httpd
BuildArch:	noarch

%if 0%{?fedora} && 0%{?fedora} >= 30
Requires:	%{name}-pytz >= 2018.9 %{name}-python3-psutil >= 5.7.0
Requires:	%{name}-python3-flask-migrate >= 2.4.0 %{name}-python3-passlib >= 1.7.2
Requires:	%{name}-python3-sshtunnel >= 0.1.4 %{name}-python3-flask-compress >= 1.4.0
Requires:	%{name}-python3-six >= 1.12.0 %{name}-python3-werkzeug >= 0.15.4
Requires:	python3-flask >= 1.0.2 python3-flask-principal >= 0.4.0
Requires:	python3-flask-wtf >= 0.14.2 python3-sqlalchemy >= 1.2.18
Requires:	python3-wtforms >= 2.2.1 python3-speaklater >= 1.3
Requires:	python3-simplejson >= 3.16.0 python3-dateutil >= 2.8.0
Requires:	python3-sqlparse >= 0.2.4 python3-flask-gravatar >= 0.5.0
Requires:	python3-flask-mail >= 0.9.1 pgadmin4-python3-flask-security-too >= 3.3.3
Requires:	python3-flask-login >= 0.4.1 python3-flask-paranoid >= 0.2
Requires:	python3-flask-sqlalchemy >= 2.3.2 python3-blinker >= 1.4
Requires:	python3-psycopg2 >= 2.8 python3-mod_wsgi
Requires:	policycoreutils-python-utils policycoreutils
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	%{name}-python3-flask >= 1.0.2 %{name}-python3-flask-sqlalchemy >= 2.3.2
Requires:	%{name}-python3-flask-wtf >= 0.14.2 %{name}-python3-sqlalchemy >= 1.2.18
Requires:	%{name}-python3-wtforms >= 2.2.1 %{name}-python3-blinker >= 1.4
Requires:	%{name}-python3-simplejson >= 3.16.0 %{name}-python3-psutil >= 5.7.0
Requires:	%{name}-python3-werkzeug >= 0.15.4 %{name}-python3-backports.csv >= 1.0.5
Requires:	%{name}-pytz >= 2018.9 %{name}-python3-sqlparse >= 0.2.4
Requires:	%{name}-python3-flask-gravatar >= 0.5.0 %{name}-python3-flask-paranoid >= 0.2
Requires:	%{name}-python3-Flask-Mail >= 0.9.1 %{name}-python3-flask-security-too >= 3.3.3
Requires:	%{name}-python3-flask-login >= 0.4.1 %{name}-python3-flask-principal >= 0.4.0
Requires:	%{name}-python3-dateutil >= 2.8.0 %{name}-python3-flask-compress >= 1.4.0
Requires:	%{name}-python3-passlib >= 1.7.2 %{name}-python3-flask-migrate >= 2.4.0
Requires:	%{name}-python3-sshtunnel >= 0.1.4 %{name}-python3-speaklater >= 1.3
Requires:	%{name}-python3-six >= 1.12.0 %{name}-python3-mod_wsgi
Requires:	python3 >= 3.6 policycoreutils-python policycoreutils python3-psycopg2 >= 2.8
%endif

%if 0%{?rhel} && 0%{?rhel} == 8
Requires:	%{name}-python3-flask >= 1.0.2
Requires:	%{name}-python3-flask-wtf >= 0.14.2 %{name}-python3-sqlalchemy >= 1.2.18
Requires:	%{name}-python3-wtforms >= 2.2.1 %{name}-python3-passlib >= 1.7.2
Requires:	%{name}-python3-simplejson >= 3.16.0 %{name}-python3-dateutil >= 2.8.0
Requires:	%{name}-python3-sqlparse >= 0.2.4 %{name}-python3-flask-gravatar >= 0.5.0
Requires:	%{name}-python3-Flask-Mail >= 0.9.1 %{name}-python3-flask-security-too >= 3.3.3
Requires:	%{name}-python3-flask-login >= 0.4.1 %{name}-python3-flask-paranoid >= 0.2
Requires:	%{name}-python3-flask-principal >= 0.4.0 %{name}-pytz >= 2018.9
Requires:	%{name}-python3-flask-migrate >= 2.4.0 %{name}-python3-six >= 1.12.0
Requires:	%{name}-python3-sshtunnel >= 0.1.4 %{name}-python3-flask-compress >= 1.4.0
Requires:	%{name}-python3-psutil >= 5.7.0 %{name}-python3-flask-sqlalchemy >= 2.3.2
Requires:	%{name}-python3-werkzeug >= 0.15.4 %{name}-python3-speaklater >= 1.3
Requires:	python3-blinker >= 1.4 python3-psycopg2 >= 2.8 python3-mod_wsgi
Requires:	python3-cryptography python3-bcrypt python3-pynacl
Requires:	policycoreutils-python-utils policycoreutils
%endif

%description -n %{name}-web
This package contains the required files to run pgAdmin4 as a web application

%package	-n %{name}-docs
Summary:	pgAdmin4 documentation
BuildArch:	noarch

%description -n %{name}-docs
Documentation of pgadmin4.

# desktop (non-gnome)
%package	-n %{name}-desktop-common
Summary:	Desktop components of pgAdmin4 for all window managers.
Requires:	%{name}-web
%if 0%{?fedora} && 0%{?fedora} >= 30
Requires:	qt5 >= 5.1
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	qt5-qtbase >= 5.9.7
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
Requires:	qt5-qtbase >= 5.1 qt5-qtbase-gui >= 5.1
%endif

%description -n %{name}-desktop-common
Desktop components of pgAdmin4 all window managers.

# desktop-gnome
%package	-n %{name}-desktop-gnome
Summary:	GNOME Desktop components of pgAdmin4
Requires:	%{name}-web
BuildArch:	noarch
Conflicts:	%{name}-desktop
Requires:	%{name}-desktop-common
%if 0%{?fedora} && 0%{?fedora} >= 30
Requires:	gnome-shell-extension-topicons-plus gnome-shell
Requires:	qt5 >= 5.1
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	gnome-shell-extension-top-icons gnome-classic-session gnome-shell
Requires:	qt5-qtbase >= 5.9.7
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
Requires:	gnome-shell-extension-appindicator gnome-shell
Requires:	qt5-qtbase >= 5.1 qt5-qtbase-gui >= 5.1
%endif

%description -n %{name}-desktop-gnome
GNOME Desktop components of pgAdmin4.

%prep
%setup -q -n %{name}-%{version}

%build
# Remove tests and regression directories, per Dave:
find . -name tests -type d -print0|xargs -0 rm -r --
%{__rm} -rf web/regression

cd runtime
export PYTHON_CONFIG=/usr/bin/python3-config
export PYTHONPATH=%{python3_sitelib}/%{name}-web/:$PYTHONPATH
export PGADMIN_PYTHON_DIR=/usr

%{QMAKE} -o Makefile pgAdmin4.pro
%{__make}
cd ../

%install
%{__rm} -rf %{buildroot}

# Install prebuilt docs
%{__install} -d -m 755 %{buildroot}%{_docdir}/%{name}-docs/en_US/html
%{__tar} zxf %{SOURCE1}
pushd %{name}-%{version}-docs
%{__cp} -pr * %{buildroot}%{_docdir}/%{name}-docs/en_US/html/
popd

%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/runtime
%{__cp} runtime/pgAdmin4 %{buildroot}%{pgadmin4instdir}/runtime

%{__install} -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{name}-web
%{__cp} -pR web/* %{buildroot}%{PYTHON_SITELIB}/%{name}-web

# Install Apache sample config file
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
%{__sed} -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE2} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%endif
# On RHEL 7, also use our own packaged mod_wsgi, built against Python 3.
%if 0%{?rhel} == 7
%{__sed} -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' -e 's@modules/mod_wsgi.so@modules/pgadmin4-python3-mod_wsgi.so@g' < %{SOURCE2} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%endif

# Install Apache config script
%{__install} -d %{buildroot}%{pgadmin4instdir}/bin
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE7} > "%{buildroot}%{pgadmin4instdir}/bin/%{name}-web-setup.sh"

# Install desktop file, and its icon
%{__install} -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{name}-web/pgadmin/static/img/
%{__install} -m 755 runtime/pgAdmin4.ico %{buildroot}%{PYTHON_SITELIB}/%{name}-web/pgadmin/static/img/
%{__install} -d %{buildroot}%{_datadir}/applications/
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE4} > "%{buildroot}%{_datadir}/applications/%{name}.desktop"

# Install QT conf file.
# Directories are different on RHEL 7 and Fedora 24+.
%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
# Fedora 24+
%{__install} -d "%{buildroot}%{_sysconfdir}/xdg/pgadmin/"
%{__sed} -e 's@PYTHONSITELIB64@%{PYTHON_SITELIB64}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE6} > "%{buildroot}%{_sysconfdir}/xdg/pgadmin/%{name}.conf"
%else
# CentOS 7
%{__install} -d "%{buildroot}%{_sysconfdir}/pgadmin/"
%{__sed} -e 's@PYTHONSITELIB64@%{PYTHON_SITELIB64}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE6} > "%{buildroot}%{_sysconfdir}/pgadmin/%{name}.conf"
%endif

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__sed} -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' -e 's@OSPYTHON@%{__ospython}@g'<%{SOURCE8} > "%{buildroot}%{_unitdir}/%{name}.service"
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

cd %{buildroot}%{PYTHON_SITELIB}/%{name}-web
%{__rm} -f %{name}.db
echo "HELP_PATH = '/usr/share/doc/%{name}-docs/en_US/html'" > config_distro.py
# Disable upgrade check in the packages:
echo "UPGRADE_CHECK_ENABLED = False" >> config_distro.py

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post -n %{name}-desktop-common
if [ $1 > 1 ] ; then
 %{__ln_s} %{pgadmin4instdir}/runtime/pgAdmin4 %{_bindir}/pgadmin4 >/dev/null 2>&1 || :
fi

%post -n %{name}-desktop-gnome
	# Enable the extension. Don't throw an error if it is already enabled.
%if 0%{?fedora} >= 30
	gnome-shell-extension-tool -e topicons-plus >/dev/null 2>&1 || :
%endif
%if 0%{?rhel} == 7
	gnome-shell-extension-tool -e top-icons >/dev/null 2>&1 || :
%endif
%if 0%{?rhel} == 8
	gnome-shell-extension-tool -e appindicatorsupport@rgcjonas.gmail.com >/dev/null 2>&1 || :
%endif

%postun
# Remove symlink only during uninstall
if [ $1 -gt 0 ] ; then
	unlink %{_bindir}/pgadmin4 >/dev/null 2>&1 || :
fi

 /bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)

%files -n %{name}-web
%defattr(-,root,root,-)
%dir %{PYTHON_SITELIB}/%{name}-web/
%{PYTHON_SITELIB}/%{name}-web/*
%attr(700,root,root) %{pgadmin4instdir}/bin/%{name}-web-setup.sh
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service

%files -n %{name}-docs
%defattr(-,root,root,-)
%doc	%{_docdir}/%{name}-docs/*

%files -n %{name}-desktop-common
%defattr(-,root,root,-)
%{pgadmin4instdir}/runtime/pgAdmin4
%{_datadir}/applications/%{name}.desktop
%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
%{_sysconfdir}/xdg/pgadmin/%{name}.conf
%else
%{_sysconfdir}/pgadmin/%{name}.conf
%endif

%files -n %{name}-desktop-gnome
%defattr(-,root,root,-)

%changelog
* Fri Aug 7 2020 - Devrim Gündüz <devrim@gunduz.org> 4.24-1
- Update to 4.24
- Update RHEL 7 dependencies for changes in 4.24

* Thu May 28 2020 - Devrim Gündüz <devrim@gunduz.org> 4.22-1
- Update to 4.22

* Fri May 1 2020 - Devrim Gündüz <devrim@gunduz.org> 4.21-2
- Update dependencies for 4.21

* Wed Apr 29 2020 - Devrim Gündüz <devrim@gunduz.org> 4.21-1
- Update to 4.21
- Add a temp patch for F-32 builds. This patch will disappear
  in next pgAdmin4 release.

* Wed Apr 1 2020 - Devrim Gündüz <devrim@gunduz.org> 4.20-1
- Update to 4.20

* Tue Mar 10 2020 - Devrim Gündüz <devrim@gunduz.org> 4.19-4
- Require desktop tray extension names or RHEL 7 and 8.
- Add dependencies for the setup script. Noted when testing
  on minimal installation.
- Remove RHEL 6 portions.

* Mon Mar 9 2020 - Devrim Gündüz <devrim@gunduz.org> 4.19-3
- Add python3 dependency to all distros

* Fri Mar 6 2020 - Devrim Gündüz <devrim@gunduz.org> 4.19-2
- Fix server mode on RHEL 7

* Tue Mar 3 2020 - Devrim Gündüz <devrim@gunduz.org> 4.19-1
- Update to 4.19

* Fri Feb 28 2020 - Devrim Gündüz <devrim@gunduz.org> 4.18-2
- Initial attempt to move to Python3 on RHEL 7
- Update various dependencies for the upcoming 4.19
- Remove obsoleted dependencies

* Wed Feb 5 2020 - Devrim Gündüz <devrim@gunduz.org> 4.18-1
- Update to 4.18

* Mon Jan 27 2020 - Devrim Gündüz <devrim@gunduz.org> 4.17-2
- Final RHEL 8 fixes, per Svensson Peter.

* Sat Jan 25 2020 - Devrim Gündüz <devrim@gunduz.org> 4.17-1
- Update to 4.17
- More RHEL 8 fixes

* Wed Jan 1 2020 - Devrim Gündüz <devrim@gunduz.org> 4.16-2
- Fix a dependency for RHEL 8
- Clean references to unsupported distros

* Thu Dec 12 2019 - Devrim Gündüz <devrim@gunduz.org> 4.16-1
- Update to 4.16

* Sat Nov 23 2019 - Devrim Gündüz <devrim@gunduz.org> 4.15-1
- Update to 4.15

* Thu Sep 19 2019 - Devrim Gündüz <devrim@gunduz.org> 4.13-1
- Update to 4.13

* Thu Aug 22 2019 - Devrim Gündüz <devrim@gunduz.org> 4.12-1
- Update to 4.12
- Remove the patch that was temporarily added in 4.11.
- Do not build docs -- use prebuilt one.

* Tue Jul 23 2019 - Devrim Gündüz <devrim@gunduz.org> 4.11-1
- Update to 4.11
- Add a patch to fix feature tests on RHEL 7. Contributed by Akshay Joshi.

* Thu Jul 11 2019 - Devrim Gündüz <devrim@gunduz.org> 4.10-2
- Fix werkzeug dependency.

* Wed Jul 3 2019 - Devrim Gündüz <devrim@gunduz.org> 4.10-1
- Update to 4.10

* Mon Jun 3 2019 - Devrim Gündüz <devrim@gunduz.org> 4.8-1
- Update to 4.8

* Thu May 30 2019 - Devrim Gündüz <devrim@gunduz.org> 4.7-2
- Rebuild

* Tue May 28 2019 - Devrim Gündüz <devrim@gunduz.org> 4.7-1
- Update to 4.7
- Remove version numbers from obsoletes, as I'm too lazy to find out
  what exactly we are obsoleting. Per https://redmine.postgresql.org/issues/4299

* Fri May 24 2019 - Devrim Gündüz <devrim@gunduz.org> 4.6-3
- Add SELinux bits to the setup script, per report from Michael Monerau.

* Thu May 23 2019 - Devrim Gündüz <devrim@gunduz.org> 4.6-2
- Fix setup script. Per report from Michael Monerau.

* Sun May 19 2019 - Devrim Gündüz <devrim@gunduz.org> 4.6-1
- Update to 4.6

* Thu Apr 18 2019 - Devrim Gündüz <devrim@gunduz.org> 4.5-1
- Update to 4.5

* Fri Mar 8 2019 - Devrim Gündüz <devrim@gunduz.org> 4.3-1
- Update to 4.3

* Mon Feb 11 2019 - Devrim Gündüz <devrim@gunduz.org> 4.2-2
- Disable upgrade checks.
- Add a unit file. Per https://redmine.postgresql.org/issues/3817.

* Fri Feb 8 2019 - Devrim Gündüz <devrim@gunduz.org> 4.2-1
- Update to 4.2

* Sun Jan 20 2019 - Devrim Gündüz <devrim@gunduz.org> 4.1-2
- Create pgadmin4 symlink properly.
- Add a patch for RHEL7, to be removed in 4.2

* Sat Jan 19 2019 - Devrim Gündüz <devrim@gunduz.org> 4.1-1
- Update to 4.1

* Mon Jan 14 2019 - Devrim Gündüz <devrim@gunduz.org> 4.0-1
- Update to 4.0

* Tue Dec 4 2018 - Devrim Gündüz <devrim@gunduz.org> 3.6-1
- Update to 3.6
- Remove patch5, it is now in upstream.

* Mon Nov 5 2018 - Devrim Gündüz <devrim@gunduz.org> 3.5-2
- Add a temp patch to fix setup script issue.
- Add missing dependencies
- Update flask mininum version to 0.12.4 .
- Update tmpfiles.d file, /var/run is now a legacy directory.

* Thu Nov 1 2018 - Devrim Gündüz <devrim@gunduz.org> 3.5-1
- Update to 3.5

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.4-1.1
- Rebuild against PostgreSQL 11.0

* Fri Oct 5 2018 - Devrim Gündüz <devrim@gunduz.org> 3.4-1
- Update to 3.4

* Thu Sep 6 2018 - Devrim Gündüz <devrim@gunduz.org> 3.3-1
- Update to 3.3

* Thu Aug 9 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2

* Thu Aug 2 2018 - John Harvey <john.harvey@crunchydata.com> 3.1-2
- Update Obsoletes

* Tue Jun 26 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-6
- Move symlink creation into desktop-common subpackage.

* Wed Apr 18 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-5
- Rebuilt

* Wed Apr 18 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-4
- Split desktop components into their own subpackages. Move files
  of the main package to desktop-common package.
- Add dependency to alembic for setup script.

* Tue Apr 17 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-3
- Fix setup script.

* Mon Apr 16 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-2
- Remove -v3 from package name. That made upgrades harder.
- No longer use alternatives, we don't allow parallel installation already.

* Wed Mar 21 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0
- Use Python 3.4 from EPEL on RHEL 6, and also use PY3 versions
  of our dependencies on RHEL 6 as well. Per Dave.
- Remove unit file and references to it. Per Dave.

* Wed Jan 10 2018 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1
- Remove patch3 -- now applied to upstream.

* Fri Sep 29 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0 gold.

* Thu Sep 21 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-rc2-2
- Require our flask on PY2 environment,	per report from	Fahar.

* Mon Sep 18 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-rc2-1
- Update to 2.0 rc2
- Remove obsoleted patch5

* Fri Sep 15 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-rc1-2
- Add flask-paranoid to Requires, too.

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-rc1-1
- Update to 2.0 rc1

* Thu Jul 27 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6-3
-  On PPC, before starting main application, need to set
   'QT_X11_NO_MITSHM=1' to make the runtime work. Add this patch
   to fix PPC builds.

* Thu Jul 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6-2
- Revert the fix applied for #2496 which breaks desktop mode.

* Tue Jul 11 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6-1
- Update to 1.6

* Thu Jul 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.5-5
- More fixes to -web package, per John Harvey.
- Replace pgadmin4 with %%{name} macros.

* Tue Jul 4 2017 - Devrim Gündüz <devrim@gunduz.org> 1.5-4
- Various fixes to -web package:
  - Create /var/lib/pgadmin directory, and add config_local.py
    which includes references to that directory. Per Josh.
    Fixes #2495.
- Fix systemd unit file, so that pgadmin4 unit is run by apache,
  not root. Per Josh. Fixes #2495.

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.5-3
- Add pgadmin4-python-backports-csv dependency for RHEL 6 and RHEL 7.

* Wed May 31 2017 - Devrim Gündüz <devrim@gunduz.org> 1.5-2
- Add new dependencies.

* Thu May 18 2017 - Devrim Gündüz <devrim@gunduz.org> 1.5-1
- Update to 1.5

* Thu Apr 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4
- Adjust dependencies for new package naming.
- Remove patch1, now it is in upstream.

* Fri Mar 17 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3-2
- Apply patches to spec file, to build and run pgadmin4
  on RHEL 6.

* Wed Mar 8 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3
- Add a temp patch (patch1) to fix a Python 3.5 regression issue.
- Remove obsoleted patches

* Tue Feb 7 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2-3
* Fix Fedora 25 issues, per Dave Page:
 - Install runtime conf file under /etc/xdg/pgadmin4
 - Add qt5-qtwebengine as BR and R.
- Use more macros in spec file.

* Tue Feb 7 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2-2
- Fix dependency issue on RHEL 7.

* Tue Feb 7 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2
- Various fixes to spec file and qt patch. Patch from Dave Page.

* Tue Nov 15 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-5
- Add a patch to conf.py to pick up the default theme, instead
  of classic theme. We need this to build docs on older sphinx
  versions.
- Modify the spec file a bit to be able to apply the patch.

* Sat Nov 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-4
- Use the actual icon in menu, per Dave.
- Add more BR for -docs subpackage.

* Fri Nov 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-3
- Fix -docs content, install html files.

* Fri Nov 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-2
- Change the package name, so that multiple major versions
  can be installed in parallel.
- Change the default install dir. Per Dave.
- Fix desktop mode, by fixing pgadmin4.conf QT conf file.
  Per Dave Page.
- Remove config_local.py, per Dave.
- Add MINIFY_HTML to config_distro.py, per Dave.
- Install Apache config file as a sample file, leave the rest
  to the user. Per Dave.
- Install pgadmin4 binary under /usr/bin, with alternatives.

* Fri Nov 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Mon Oct 10 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-4
- Fix Exec path in desktop file.

* Mon Oct 10 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-3
- Fix more packaging issues:
  - Add dependency for mod_wsgi, per report from Josh Berkus.
  - Add QT conf file for desktop application to work. Per Dave Page.
  - Add -docs subpacage as Requires: to main package. Per Dave.

* Thu Oct 6 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Fix various packaging issues:
  - Install config_local.py with some default values. Fixes #1820.
  - Fix desktop file. Fixes #1829.

* Wed Sep 28 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Update to pgadmin4 1.0 Gold!

* Wed Sep 14 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-6
- Fix Type in systemd unit file.

* Mon Sep 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-5
- Add .desktop file
- Move contents of config_local.py to config_distro.py, per Dave.
- Fix typo in -dateutil dependency

* Sun Sep 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-4
- Add actual dependencies for packages.

* Sun Sep 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-3
- Properly detect python sitelib

* Sat Sep 10 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-2
- Add httpd config file, per Dave.
- Add unit file support for systemd distros.

* Fri Sep 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-1
- Initial spec file, based on Sandeep Thakkar's spec.
