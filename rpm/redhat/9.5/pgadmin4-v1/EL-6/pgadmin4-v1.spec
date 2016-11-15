%global sname pgadmin4
%global pgadminmajorversion 1
%global	pgadmin4instdir /usr/pgadmin4-v%{pgadminmajorversion}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python3_sitelib}
%global PYTHON_SITELIB64 %{python3_sitelib64}
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python2_sitelib}
%global PYTHON_SITELIB64 %{python2_sitelib64}
%endif

Name:		%{sname}-v%{pgadminmajorversion}
Version:	%{pgadminmajorversion}.1
Release:	5%{?dist}
Summary:	Management tool for PostgreSQL
Group:		Applications/Databases
License:	PostgreSQL
URL:		https://www.pgadmin.org
Source0:	https://download.postgresql.org/pub/pgadmin3/%{sname}/v%{version}/source/%{sname}-%{version}.tar.gz
Source1:	%{sname}.conf
Source2:	%{sname}.service.in
Source3:	%{sname}.tmpfiles.d
Source4:	%{sname}.desktop.in
Source6:	%{sname}.qt.conf.in
# Adding this patch to be able to build docs on < Fedora 24.
Patch0:		%{sname}-sphinx-theme.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	mesa-libGL-devel
BuildRequires:	gcc-c++
# These are for docs:
BuildRequires:	python-flask-security, python-flask-gravatar, python-flask-mail
BuildRequires:	python-flask-wtf, django-htmlmin, python-blinker
BuildRequires:	python-beautifulsoup4, python-dateutil, python-simplejson

Requires:	%{name}-web
%if 0%{?with_python3}
BuildRequires:	qt5-qtbase-devel >= 5.1
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	python2-passlib
%global QMAKE	/usr/bin/qmake-qt5
%else
BuildRequires:	qt-devel >= 4.6
BuildRequires:	qtwebkit-devel
BuildRequires:	python-passlib
%global QMAKE	/usr/bin/qmake-qt4
%endif

%if 0%{?with_python3}
BuildRequires:	python3-devel
Requires:	python3 >= 3.3
%else
BuildRequires:	python-devel
Requires:	python >= 2.6
%endif

%if 0%{?with_python3}
Requires:	qt >= 5.1
%else
Requires:	qt >= 4.6
%endif

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
pgAdmin 4 is a rewrite of the popular pgAdmin3 management tool for the PostgreSQL
(http://www.postgresql.org) database.
pgAdmin 4 is written as a web application in Python, using jQuery and Bootstrap
for the client side processing and UI. On the server side, Flask is being utilised.

Although developed using web technologies, we intend for pgAdmin 4 to be usable
either on a web server using a browser, or standalone on a workstation. The
runtime/ subdirectory contains a QT based runtime application intended to allow
this - it is essentially a browser and Python interpretor in one package which
will be capable of hosting the Python application and presenting it to the user
as a desktop application.

%package	-n %{name}-web
Summary:	pgAdmin4 web package
Requires:	%{name}-docs
BuildArch:	noarch
%if 0%{?with_python3}
Requires:	python3-babel >= 1.3
Requires:	python3-flask >= 0.11.1
Requires:	python3-flask-sqlalchemy >= 2.1
Requires:	python3-flask-wtf >= 0.12
Requires:	python3-jinja2 >= 2.7.3
Requires:	python3-markupsafe >= 0.23
Requires:	python3-sqlalchemy >= 1.0.14
Requires:	python3-wtforms >= 2.0.2
Requires:	python3-beautifulsoup4 >= 4.4.1
Requires:	python3-blinker >= 1.3
Requires:	python3-html5lib >= 1.0b3
Requires:	python3-itsdangerous >= 0.24
Requires:	python3-psycopg2 >= 2.6.2
Requires:	python3-six >= 1.9.0
Requires:	python3-crypto >= 2.6.1
Requires:	python3-simplejson >= 3.6.5
Requires:	python3-dateutil >= 2.5.0
Requires:	python3-werkzeug >= 0.9.6
Requires:	python3-sqlparse >= 0.1.19
Requires:	python3-flask-babel >= 0.11.1
Requires:	python3-passlib >= 1.6.2
Requires:	python3-flask-gravatar >= 0.4.2
Requires:	python3-flask-mail >= 0.9.1
Requires:	python3-flask-security >= 1.7.5
Requires:	python3-flask-login >= 0.3.2
Requires:	python3-flask-principal >= 0.4.0
Requires:	django-htmlmin >= 0.8.0
Requires:	python-wsgiref >= 0.1.2
Requires:	pytz >= 2014.10
Requires:	python3-click
Requires:	python3-extras >= 0.0.3
Requires:	python3-fixtures >= 2.0.0
Requires:	python3-pyrsistent >= 0.11.13
Requires:	python3-mimeparse >= 1.5.1
Requires:	python3-speaklater >= 1.3
Requires:	python3-mod_wsgi
# TODO: Confirm dependencies of: testscenarios, testtools, traceback2, unittest2
%else
Requires:	python-babel >= 1.3
Requires:	python-flask >= 0.11.1
Requires:	python-flask-sqlalchemy >= 2.1
Requires:	python-flask-wtf >= 0.12
Requires:	python-jinja2 >= 2.7.3
Requires:	python-markupsafe >= 0.23
Requires:	python-sqlalchemy >= 1.0.14
Requires:	python-wtforms >= 2.0.2
Requires:	python-beautifulsoup4 >= 4.4.1
Requires:	python-blinker >= 1.3
Requires:	python-html5lib >= 1.0b3
Requires:	python-itsdangerous >= 0.24
Requires:	python-psycopg2 >= 2.6.2
Requires:	python-six >= 1.9.0
Requires:	python-crypto >= 2.6.1
Requires:	python-simplejson >= 3.6.5
Requires:	python-dateutil >= 2.5.0
Requires:	python-werkzeug >= 0.9.6
Requires:	pytz >= 2014.10
Requires:	python-sqlparse >= 0.1.19
Requires:	python-flask-babel >= 0.11.1
Requires:	python-passlib >= 1.6.2
Requires:	python-flask-gravatar >= 0.4.2
Requires:	python-flask-mail >= 0.9.1
Requires:	python-flask-security >= 1.7.5
Requires:	python-flask-login >= 0.3.2
Requires:	python-flask-principal >= 0.4.0
Requires:	django-htmlmin >= 0.8.0
Requires:	python-wsgiref >= 0.1.2
Requires:	python-click
Requires:	python-extras >= 0.0.3
Requires:	python-fixtures >= 2.0.0
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	python-importlib >= 1.0.3
%endif
Requires:	python-pyrsistent >= 0.11.13
Requires:	python-mimeparse >= 1.5.1
Requires:	python-speaklater >= 1.3
Requires:	mod_wsgi
%endif

%description    -n %{name}-web
This package contains the required files to run pgAdmin4 as a web application

%package	-n %{name}-docs
Summary:	pgAdmin4 documentation
BuildArch:	noarch

%description -n %{name}-docs
Documentation of pgadmin4.

%prep
%setup -q -n %{sname}-%{version}
# Apply this patch only to RHEL 6,7  and Fedora 23:
%if 0%{?fedora} <= 23 || 0%{?rhel} <= 7
%patch0 -p0
%endif

%build
cd runtime
%if 0%{?with_python3}
export PYTHON_CONFIG=/usr/bin/python3-config
%else
export PYTHON_CONFIG=/usr/bin/python-config
%endif
%{QMAKE} -o Makefile pgAdmin4.pro
make
cd ../
make docs

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{_docdir}/%{name}-docs/en_US/html
%{__cp} -pr docs/en_US/_build/html/* %{buildroot}%{_docdir}/%{name}-docs/en_US/html/

install -d -m 755 %{buildroot}%{pgadmin4instdir}/runtime
%{__cp} runtime/pgAdmin4 %{buildroot}%{pgadmin4instdir}/runtime

install -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{sname}-web
%{__cp} -pR web/* %{buildroot}%{PYTHON_SITELIB}/%{sname}-web

# Install Apache sample config file
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
sed -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE1}  > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf.sample

# Install desktop file, and its icon
install -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{sname}-web/pgadmin/static/img/
install -m 755 runtime/pgAdmin4.ico %{buildroot}%{PYTHON_SITELIB}/%{sname}-web/pgadmin/static/img/
install -d %{buildroot}%{_datadir}/applications/
sed -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE4} > %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install QT conf file
# This directory will/may change in future releases.
install -d "%{buildroot}%{_sysconfdir}/pgAdmin Development Team/"
sed -e 's@PYTHONSITELIB64@%{PYTHON_SITELIB64}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE6} > "%{buildroot}%{_sysconfdir}/pgAdmin Development Team/pgAdmin 4.conf"

# Install unit file/init script
%if %{systemd_enabled}
# This is only for systemd supported distros:
install -d %{buildroot}%{_unitdir}
sed -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE2} > %{buildroot}%{_unitdir}/%{name}.service
%else
# Reserved for init script
:
%endif
%if %{systemd_enabled}
# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}/%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf
%endif
cd %{buildroot}%{PYTHON_SITELIB}/%{sname}-web
%{__rm} -f %{name}.db
echo "SERVER_MODE = False" > config_distro.py
echo "MINIFY_HTML = False" >> config_distro.py
echo "HELP_PATH = '/usr/share/doc/pgadmin4-v1-docs/en_US/html'" >> config_distro.py
echo "
[General]
ApplicationPath=%{PYTHON_SITELIB}/%{name}-web
PythonPath=%{PYTHON_SITELIB};%{PYTHON_SITELIB64}
" > %{buildroot}%{pgadmin4instdir}/runtime/%{sname}.ini

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install /usr/bin/%{sname} %{sname} %{pgadmin4instdir}/runtime/pgAdmin4 %{pgadminmajorversion}
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post %{name}.service
   %tmpfiles_create
  %else
   :
   #chkconfig --add %%{name}
  %endif
fi

%preun
if [ $1 -eq 0 ] ; then
	%{_sbindir}/update-alternatives --remove %{sname} %{pgadmin4instdir}/runtime/pgAdmin4
%if %{systemd_enabled}
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
%else
	:
	#/sbin/service %%{name} condstop >/dev/null 2>&1
	#chkconfig --del %%{name}
%endif
fi

%postun
%if %{systemd_enabled}
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 :
 #sbin/service %%{name} >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %{systemd_enabled}
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
 %else
    :
	#/sbin/service %%{name} condrestart >/dev/null 2>&1
 %endif
fi

%files
%defattr(-,root,root,-)
%{pgadmin4instdir}/runtime/pgAdmin4
%{pgadmin4instdir}/runtime/%{sname}.ini
%{_datadir}/applications/%{name}.desktop
"%{_sysconfdir}/pgAdmin Development Team/pgAdmin 4.conf"

%files -n %{name}-web
%defattr(-,root,root,-)
%dir %{PYTHON_SITELIB}/%{sname}-web/
%{PYTHON_SITELIB}/%{sname}-web/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%if %{systemd_enabled}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%endif

%files -n %{name}-docs
%defattr(-,root,root,-)
%doc	%{_docdir}/%{name}-docs/*

%changelog
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
