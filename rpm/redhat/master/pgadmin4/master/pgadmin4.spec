%global debug_package %{nil}
%global sname pgadmin4
%global pgadminmajorversion 3
%global	pgadmin4instdir /usr/%{sname}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%endif

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python3_sitelib}
%global PYTHON_SITELIB64 %{python3_sitelib64}
%endif
%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3.4
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python2_sitelib}
%global PYTHON_SITELIB64 %{python2_sitelib64}
%endif
%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python2_sitelib}
%global PYTHON_SITELIB64 %{python2_sitelib64}
%endif

Name:		%{sname}
Version:	%{pgadminmajorversion}.0
Release:	4%{?dist}
Summary:	Management tool for PostgreSQL
Group:		Applications/Databases
License:	PostgreSQL
URL:		https://www.pgadmin.org
Source0:	https://download.postgresql.org/pub/pgadmin/%{sname}/v%{version}/source/%{sname}-%{version}.tar.gz
Source1:	%{sname}.conf
Source3:	%{sname}.tmpfiles.d
Source4:	%{sname}.desktop.in
Source6:	%{sname}.qt.conf.in
Source7:	%{sname}-web-setup.sh
# Adding this patch to be able to build docs on < Fedora 24.
Patch0:		%{sname}-sphinx-theme.patch
Patch2:		%{sname}-rhel6-sphinx.patch
Patch4:		%{sname}-rhel7-sphinx.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:	pgadmin4-v2 <= 2.0 pgadmin4-v3 <= 3.0

BuildRequires:	gcc-c++

Requires:	%{name}-web

%if 0%{?fedora}
BuildRequires:	%{sname}-python3-passlib >= 1.7.1 %{sname}-python3-dateutil %{sname}-python3-simplejson >= 3.13.2
BuildRequires:	%{sname}-python3-Flask-Mail %{sname}-python3-flask-gravatar
BuildRequires:	%{sname}-python3-flask-babel %{sname}-python3-flask-htmlmin
BuildRequires:	%{sname}-python3-flask-security >= 3.0.0 %{sname}-python3-flask-principal
BuildRequires:	%{sname}-python3-flask-wtf %{sname}-python3-flask >= 0.12.2
BuildRequires:	%{sname}-python3-flask-paranoid >= 0.1 %{sname}-python3-flask-login >= 0.3.2
BuildRequires:	%{sname}-python3-sqlalchemy >= 1.2.5 %{sname}-python3-flask-babelex
BuildRequires:	qt5-qtbase-devel >= 5.1 python3-sphinx python3-pbr >= 3.1.1 python3-devel
BuildRequires:	python3-itsdangerous python3-blinker python3-flask-sqlalchemy
BuildRequires:	python3-sphinx python3-pbr >= 3.1.1 python3-linecache2 >= 1.0.0
%global QMAKE	/usr/bin/qmake-qt5
%endif

%if 0%{?rhel} == 6
BuildRequires:	qt5-qtbase-devel >= 5.1
BuildRequires:	%{sname}-python3-dateutil %{sname}-python3-simplejson >= 3.13.2
BuildRequires:	%{sname}-python3-Flask-Mail %{sname}-python3-flask-gravatar
BuildRequires:	%{sname}-python3-flask-babel %{sname}-python3-flask-htmlmin
BuildRequires:	%{sname}-python3-flask-security >= 3.0.0 %{sname}-python3-flask-principal
BuildRequires:	%{sname}-python3-flask-wtf %{sname}-python3-flask >= 0.12.2
BuildRequires:	%{sname}-python3-flask-paranoid >= 0.1 %{sname}-python3-flask-login >= 0.3.2
BuildRequires:	%{sname}-python3-itsdangerous %{sname}-python3-blinker %{sname}-python3-flask-babelex
BuildRequires:	%{sname}-python3-flask-sqlalchemy %{sname}-python3-pbr >= 3.1.1
BuildRequires:	%{sname}-python3-passlib >= 1.7.1 %{sname}-python3-sqlalchemy >= 1.2.5
BuildRequires:	%{sname}-python3-pbr >= 3.1.1 %{sname}-python3-linecache2 >= 1.0.0
BuildRequires:	python34-devel python34-sqlalchemy python-sphinx10
%global QMAKE	/usr/bin/qmake-qt5
%endif

%if 0%{?rhel} == 7
BuildRequires:	%{sname}-python-flask >= 0.12.2 %{sname}-python-flask-babel
BuildRequires:	%{sname}-python-itsdangerous >= 0.24 %{sname}-python-flask-htmlmin
BuildRequires:	%{sname}-python-flask-security >= 3.0.0 %{sname}-python-flask-principal
BuildRequires:	%{sname}-python-flask-login >= 0.3.2 %{sname}-python-simplejson >= 3.13.2
BuildRequires:	%{sname}-python-blinker %{sname}-python-flask-wtf %{sname}-python-flask-babelex
BuildRequires:	%{sname}-python-flask-sqlalchemy %{sname}-python-Flask-Mail
BuildRequires:	%{sname}-python-dateutil %{sname}-python-flask-gravatar
BuildRequires:	%{sname}-python-flask-paranoid >= 0.1 %{sname}-python-pbr >= 3.1.1
BuildRequires:	%{sname}-python-passlib >= 1.7.1 %{sname}-python-sqlalchemy >= 1.2.5
BuildRequires:	python-devel python-sphinx python-linecache2 >= 1.0.0
BuildRequires:	mesa-libGL-devel qt-devel >= 4.6
%global QMAKE	/usr/bin/qmake-qt4
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	Mesa-libGL-devel
BuildRequires:	libqt4-devel
Requires:  libqt4 >= 4.6
%global QMAKE  /usr/bin/qmake
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
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

Obsoletes:	pgadmin4-v2-web <= 2.0 pgadmin4-v3-web <= 3.0

%if 0%{?fedora}
Requires:	%{sname}-python3-flask-htmlmin >= 1.2 %{sname}-python3-flask >= 0.12.2
Requires:	%{sname}-python3-flask-wtf >= 0.12 %{sname}-python3-sqlalchemy >= 1.2.5
Requires:	%{sname}-python3-wtforms >= 2.0.2 %{sname}-python3-html5lib >= 1.0.1
Requires:	%{sname}-python3-simplejson >= 3.13.2 %{sname}-python3-dateutil >= 2.7.2
Requires:	%{sname}-python3-sqlparse >= 0.2.4 %{sname}-python3-flask-gravatar >= 0.5.0
Requires:	%{sname}-python3-flask-babel >= 0.11.1 %{sname}-python3-passlib >= 1.7.1
Requires:	%{sname}-python3-Flask-Mail >= 0.9.1 %{sname}-python3-flask-security >= 3.0.0
Requires:	%{sname}-python3-flask-login >= 0.3.2 %{sname}-python3-flask-paranoid >= 0.1
Requires:	%{sname}-python3-flask-principal >= 0.4.0 %{sname}-pytz >= 2018.3 python3-click
Requires:	%{sname}-python3-pyrsistent >= 0.14.2 %{sname}-python3-flask-migrate >= 2.1.1
Requires:	python3-flask-sqlalchemy >= 2.1 python3-babel >= 2.3.4
Requires:	python3-jinja2 >= 2.7.3	python3-markupsafe >= 0.23
Requires:	python3-beautifulsoup4 >= 4.4.1 python3-pbr >= 3.1.1
Requires:	python3-blinker >= 1.3 python3-itsdangerous >= 0.24
Requires:	python3-psycopg2 >= 2.7.4 python3-linecache2 >= 1.0.0
Requires:	python3-six >= 1.9.0 python3-crypto >= 2.6.1 python3-werkzeug >= 0.9.6
Requires:	python3-extras >= 1.0.0	python3-fixtures >= 2.0.0
Requires:	python3-mimeparse >= 1.6.0 python3-speaklater >= 1.3
Requires:	python3-mod_wsgi python3-unittest2 python3-alembic
%endif

%if 0%{?rhel} == 6
Requires:	%{sname}-python3-passlib >= 1.7.1 %{sname}-python3-flask-migrate >= 2.1.1
Requires:	%{sname}-python3-crypto >= 2.6.1 %{sname}-python3-speaklater >= 1.3
Requires:	%{sname}-python3-html5lib >= 1.0.1 %{sname}-python3-fixtures >= 2.0.0
Requires:	%{sname}-python3-babel >= 2.3.4 %{sname}-python3-flask >= 0.12.2
Requires:	%{sname}-python3-flask-htmlmin >= 1.2 %{sname}-python3-flask-sqlalchemy >= 2.1
Requires:	%{sname}-python3-flask-wtf >= 0.12 %{sname}-python3-wtforms >= 2.0.2
Requires:	%{sname}-python3-beautifulsoup4 >= 4.4.1 %{sname}-python3-blinker >= 1.3
Requires:	%{sname}-python3-itsdangerous >= 0.24 %{sname}-python3-html5lib >= 1.0.1
Requires:	%{sname}-python3-simplejson >= 3.13.2 %{sname}-python3-dateutil >= 2.7.2
Requires:	%{sname}-python3-werkzeug >= 0.9.6 %{sname}-python3-sqlparse >= 0.2.4
Requires:	%{sname}-python3-flask-babel >= 0.11.1 %{sname}-python3-passlib >= 1.7.1
Requires:	%{sname}-python3-flask-gravatar >= 0.5.0 %{sname}-python3-Flask-Mail >= 0.9.1
Requires:	%{sname}-python3-flask-security >= 3.0.0 %{sname}-python3-flask-login >= 0.3.2
Requires:	%{sname}-python3-flask-paranoid >= 0.1 %{sname}-python3-flask-principal >= 0.4.0
Requires:	%{sname}-python3-pyrsistent >= 0.14.2 %{sname}-python3-flask-migrate >= 2.1.1
Requires:	%{sname}-python3-mimeparse >= 1.6.0 %{sname}-python3-pbr >= 3.1.1
Requires:	%{sname}-python3-linecache2 >= 1.0.0 %{sname}-python3-sqlalchemy >= 1.2.5
Requires:	%{sname}-pytz >= 2018.3 %{sname}-python3-click %{sname}-python3-extras >= 1.0.0
Requires:	python34 >= 3.4 python-importlib >= 1.0.3 python-unittest2
Requires:	python34-jinja2 >= 2.7.3 python34-markupsafe >= 0.23
Requires:	python-psycopg2 >= 2.7.4 python34-six >= 1.9.0
Requires:	mod_wsgi python-unittest2
%endif

%if 0%{?rhel} == 7
Requires:	%{sname}-python-babel >= 2.3.4 %{sname}-python-flask >= 0.12.2
Requires:	%{sname}-python-flask-htmlmin >= 1.2 %{sname}-python-flask-sqlalchemy >= 2.1
Requires:	%{sname}-python-flask-wtf >= 0.12 %{sname}-python-jinja2 >= 2.7.3
Requires:	%{sname}-python-markupsafe >= 0.23 %{sname}-python-sqlalchemy >= 1.2.5
Requires:	%{sname}-python-wtforms >= 2.0.2 %{sname}-python-beautifulsoup4 >= 4.4.1
Requires:	%{sname}-python-blinker >= 1.3 %{sname}-python-flask-paranoid >= 0.1
Requires:	%{sname}-python-itsdangerous >= 0.24 %{sname}-python-simplejson >= 3.13.2
Requires:	%{sname}-python-werkzeug >= 0.9.6 %{sname}-python-backports.csv >= 1.0.5
Requires:	%{sname}-pytz >= 2018.3 %{sname}-python-sqlparse >= 0.2.4
Requires:	%{sname}-python-flask-babel >= 0.11.1 %{sname}-python-flask-gravatar >= 0.5.0
Requires:	%{sname}-python-Flask-Mail >= 0.9.1 %{sname}-python-flask-security >= 3.0.0
Requires:	%{sname}-python-flask-login >= 0.3.2 %{sname}-python-flask-principal >= 0.4.0
Requires:	%{sname}-python-dateutil >= 2.7.2 %{sname}-python-fixtures >= 2.0.0
Requires:	%{sname}-python-pyrsistent >= 0.14.2 %{sname}-python-mimeparse >= 1.6.0
Requires:	%{sname}-python-extras >= 1.0.0 %{sname}-python-flask-babelex
Requires:	%{sname}-python-passlib >= 1.7.1 %{sname}-python-flask-migrate >= 2.1.1
Requires:	%{sname}-python-pbr >= 3.1.1 %{sname}-python-html5lib >= 1.0.1
Requires:	%{sname}-python-alembic
Requires:	python >= 2.7 python-six >= 1.9.0 python-psycopg2 >= 2.7.4
Requires:	python-linecache2 >= 1.0.0 python-speaklater >= 1.3 python-click
Requires:	python-crypto >= 2.6.1 mod_wsgi
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:  pgadmin4-python-html5lib >= 1.0.1
Requires:	apache2-mod_wsgi
%endif
%endif

%description    -n %{name}-web
This package contains the required files to run pgAdmin4 as a web application

%package	-n %{name}-docs
Summary:	pgAdmin4 documentation
BuildArch:	noarch

Obsoletes:	pgadmin4-v2-docs <= 2.0 pgadmin4-v3-docs <= 3.0

%description -n %{name}-docs
Documentation of pgadmin4.

# desktop (non-gnome)
%package	-n %{name}-desktop-common
Summary:	Desktop components of pgAdmin4 for all window managers.
Requires:	%{sname}-web
BuildArch:	noarch

%description -n %{name}-desktop-common
Desktop components of pgAdmin4 all window managers.

%if 0%{?fedora}
Requires:	qt >= 5.1
%endif

%if 0%{?rhel} == 6
Requires:	qt >= 4.6
%endif

%if 0%{?rhel} == 7
Requires:	qt >= 4.6
%endif

# desktop-gnome
%package	-n %{name}-desktop-gnome
Summary:	GNOME Desktop components of pgAdmin4
Requires:	%{sname}-web
BuildArch:	noarch
Conflicts:	%{name}-desktop
Requires:	%{name}-desktop-common

%description -n %{name}-desktop-gnome
GNOME Desktop components of pgAdmin4.

%if 0%{?fedora}
Requires:	gnome-shell-extension-topicons-plus gnome-shell
%endif

%prep
%setup -q -n %{sname}-%{version}
# Apply this patch only to RHEL 6 and 7:
%if 0%{?rhel} <= 7
%patch0 -p0
%endif

# Apply this patch only to RHEL 6
%if 0%{?rhel} && 0%{?rhel} <= 6
%patch2 -p0
%endif

%if 0%{?rhel} && 0%{?rhel} >= 7
%patch4 -p0
%endif

%build
cd runtime
%if 0%{?with_python3}
export PYTHON_CONFIG=/usr/bin/python3-config
export PYTHONPATH=%{python3_sitelib}/%{sname}-web/:$PYTHONPATH
%else
export PYTHON_CONFIG=/usr/bin/python-config
export PYTHONPATH=%{python2_sitelib}/%{sname}-web/:$PYTHONPATH
%endif
%{QMAKE} -o Makefile pgAdmin4.pro
make
cd ../

# Build docs
%if 0%{?fedora} > 25
make PYTHON=/usr/bin/python3 SPHINXBUILD=/usr/bin/sphinx-build-3 docs
%endif
%if 0%{?rhel} == 6
make PYTHON=/usr/bin/python3 SPHINXBUILD=/usr/bin/sphinx-1.0-build docs
%endif
%if 0%{?rhel} == 7
make PYTHON=/usr/bin/python docs
%endif

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}%{_docdir}/%{name}-docs/en_US/html
%{__cp} -pr docs/en_US/_build/html/* %{buildroot}%{_docdir}/%{name}-docs/en_US/html/

%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/runtime
%{__cp} runtime/pgAdmin4 %{buildroot}%{pgadmin4instdir}/runtime

%{__install} -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{sname}-web
%{__cp} -pR web/* %{buildroot}%{PYTHON_SITELIB}/%{sname}-web

# Install Apache sample config file
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__sed} -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf.sample

# Install Apache config script
%{__install} -d %{buildroot}%{pgadmin4instdir}/bin
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE7} > %{buildroot}%{pgadmin4instdir}/bin/%{name}-web-setup.sh

# Install desktop file, and its icon
%{__install} -d -m 755 %{buildroot}%{PYTHON_SITELIB}/%{sname}-web/pgadmin/static/img/
%{__install} -m 755 runtime/pgAdmin4.ico %{buildroot}%{PYTHON_SITELIB}/%{sname}-web/pgadmin/static/img/
%{__install} -d %{buildroot}%{_datadir}/applications/
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g' < %{SOURCE4} > %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install QT conf file.
# Directories are different on RHEL 7 and Fedora 24+.
%if 0%{?fedora} > 25
# Fedora 24+
%{__install} -d "%{buildroot}%{_sysconfdir}/xdg/pgadmin/"
%{__sed} -e 's@PYTHONSITELIB64@%{PYTHON_SITELIB64}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE6} > "%{buildroot}%{_sysconfdir}/xdg/pgadmin/%{sname}.conf"
%else
# CentOS 7
%{__install} -d "%{buildroot}%{_sysconfdir}/pgadmin/"
%{__sed} -e 's@PYTHONSITELIB64@%{PYTHON_SITELIB64}@g' -e 's@PYTHONSITELIB@%{PYTHON_SITELIB}@g'<%{SOURCE6} > "%{buildroot}%{_sysconfdir}/pgadmin/%{sname}.conf"
%endif

%if %{systemd_enabled}
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf
%endif

cd %{buildroot}%{PYTHON_SITELIB}/%{sname}-web
%{__rm} -f %{name}.db
echo "HELP_PATH = '/usr/share/doc/%{sname}-docs/en_US/html'" > config_distro.py

%clean
%{__rm} -rf %{buildroot}

%post
%{__ln_s} %{pgadmin4instdir}/runtime/pgAdmin4 %{_bindir}/pgadmin4 >/dev/null 2>&1 || :
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   :
   %endif
   %else
   %tmpfiles_create
   %endif
  %else
   :
  %endif
fi

%post -n %{name}-desktop-gnome
%if 0%{?fedora} > 25
	# Enable the extension. Don't throw an error if it is already enabled.
	gnome-shell-extension-tool -e topicons-plus >/dev/null 2>&1 || :
%endif

%postun
# Remove symlink only during uninstall
if [ $1 -gt 0 ] ; then
	unlink %{_bindir}/pgadmin4
fi

%if %{systemd_enabled}
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 :
%endif

%files
%defattr(-,root,root,-)

%files -n %{name}-web
%defattr(-,root,root,-)
%dir %{PYTHON_SITELIB}/%{sname}-web/
%{PYTHON_SITELIB}/%{sname}-web/*
%attr(700,root,root) %{pgadmin4instdir}/bin/%{name}-web-setup.sh
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%if %{systemd_enabled}
%{_tmpfilesdir}/%{name}.conf
%endif

%files -n %{name}-docs
%defattr(-,root,root,-)
%doc	%{_docdir}/%{name}-docs/*

%files -n %{name}-desktop-common
%defattr(-,root,root,-)
%{pgadmin4instdir}/runtime/pgAdmin4
%{_datadir}/applications/%{name}.desktop
%if 0%{?fedora} > 25
%{_sysconfdir}/xdg/pgadmin/%{sname}.conf
%else
%{_sysconfdir}/pgadmin/%{sname}.conf
%endif

%files -n %{name}-desktop-gnome
%defattr(-,root,root,-)

%changelog
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
- Replace pgadmin4 with %%{sname} macros.

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
