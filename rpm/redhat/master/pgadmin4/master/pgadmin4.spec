# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0

%global debug_package %{nil}
%global pgadminmajorversion 4
%global	pgadmin4instdir /usr/%{name}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%endif

%if 0%{?fedora} > 25 || 0%{?rhel} == 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python3_sitelib}
%global PYTHON_SITELIB64 %{python3_sitelib64}
%global QMAKE  /usr/bin/qmake-qt5
%endif

%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3.4
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python2_sitelib}
%global PYTHON_SITELIB64 %{python2_sitelib64}
%global QMAKE  /usr/bin/qmake-qt5
%endif
%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global PYTHON_SITELIB %{python2_sitelib}
%global PYTHON_SITELIB64 %{python2_sitelib64}
%global QMAKE  /usr/bin/qmake-qt4
%endif

Name:		pgadmin4
Version:	%{pgadminmajorversion}.5
Release:	1%{?dist}
Summary:	Management tool for PostgreSQL
Group:		Applications/Databases
License:	PostgreSQL
URL:		https://www.pgadmin.org
Source0:	https://download.postgresql.org/pub/pgadmin/%{name}/v%{version}/source/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source3:	%{name}.tmpfiles.d
Source4:	%{name}.desktop.in
Source6:	%{name}.qt.conf.in
Source7:	%{name}-web-setup.sh
Source8:	%{name}.service.in
# Adding this patch to be able to build docs on < Fedora 24.
Patch0:		%{name}-sphinx-theme.patch
Patch2:		%{name}-rhel6-sphinx.patch
Patch4:		%{name}-rhel7-sphinx.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:	pgadmin4-v1 pgadmin4-v2 pgadmin4-v3

BuildRequires:	gcc-c++ yarn patchelf

Requires:	%{name}-web

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

# VirtualEnv BR
%if 0%{?with_python3}
BuildRequires:	python3-virtualenvwrapper python3-virtualenv python3-pip
%else
BuildRequires:	python-virtualenvwrapper python-virtualenv python-pip
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

Obsoletes:	pgadmin4-v1-web pgadmin4-v2-web pgadmin4-v3-web

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	apache2-mod_wsgi
%endif
%endif

%description    -n %{name}-web
This package contains the required files to run pgAdmin4 as a web application

%package	-n %{name}-docs
Summary:	pgAdmin4 documentation
BuildArch:	noarch

Obsoletes:	pgadmin4-v1-docs pgadmin4-v2-docs pgadmin4-v3-docs

%description -n %{name}-docs
Documentation of pgadmin4.

# desktop (non-gnome)
%package	-n %{name}-desktop-common
Summary:	Desktop components of pgAdmin4 for all window managers.
Requires:	%{name}-web
%if 0%{?fedora} || 0%{?rhel} == 8
Requires:	qt >= 5.1
%endif
%if 0%{?rhel} == 6
Requires:	qt >= 4.6
%endif
%if 0%{?rhel} == 7
Requires:	qt >= 4.6
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
%if 0%{?fedora} || 0%{?rhel} == 8
Requires:	gnome-shell-extension-topicons-plus gnome-shell
Requires:	qt >= 5.1
%endif
%if 0%{?rhel} == 6
Requires:	qt >= 4.6
%endif
%if 0%{?rhel} == 7
Requires:	qt >= 4.6
%endif

%description -n %{name}-desktop-gnome
GNOME Desktop components of pgAdmin4.

%prep
%setup -q -n %{name}-%{version}
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
mkdir -p linux-build/venv/lib

pushd linux-build
cp -rp %{_libdir}/libpython%{pyver}*.so* venv/lib/
%{_bindir}/virtualenv -p %{__ospython} venv
source $PWD/venv/bin/activate
popd
%if 0%{?rhel} == 6
prelink -u linux-build/venv/bin/python3.4
prelink -u linux-build/venv/lib/*.so*
%endif
export PATH=%{pginstdir}/bin/:$PATH

pip%{pyver} --cache-dir "~/.cache/pip%{pyver}-pgadmin" install -r requirements.txt

PYSITEPACKAGES="$PWD/linux-build/venv/lib/python%{pyver}/site-packages"
LDFLAGS="-Wl,--rpath,$PYSITEPACKAGES/psycopg2/.libs"

pip%{pyver} install -v --no-cache-dir --no-binary :all: psycopg2

rsync -zrva --exclude site-packages --exclude lib2to3 --include="*.py" --include="*/" --exclude="*" %{_libdir}/python%{pyver}/* $PWD/linux-build/venv/lib/python%{pyver}/

cp -rf %{_libdir}/python%{pyver}/lib-dynload/* linux-build/venv/lib/python%{pyver}/lib-dynload/

cd runtime
%if 0%{?with_python3}
export PYTHON_CONFIG=/usr/bin/python3-config
export PYTHONPATH=%{python3_sitelib}/%{name}-web/:$PYTHONPATH
%else
export PYTHON_CONFIG=/usr/bin/python-config
export PYTHONPATH=%{python2_sitelib}/%{name}-web/:$PYTHONPATH
%endif
PGADMIN_LDFLAGS="-Wl,--rpath,%{buildroot}%{pgadmin4instdir}/venv/lib"; export PGADMIN_LDFLAGS
%{QMAKE} -o Makefile pgAdmin4.pro
%{__make}
cd ../

# Build JS libraries
%{__make} install-node
%{__make} bundle

# Build docs
%if 0%{?fedora} > 25 || 0%{?rhel} == 8
%{__make} PYTHON=/usr/bin/python3 SPHINXBUILD=/usr/bin/sphinx-build-3 docs
%endif
%if 0%{?rhel} == 6
%{__make} PYTHON=/usr/bin/python3 SPHINXBUILD=/usr/bin/sphinx-1.0-build docs
%endif
%if 0%{?rhel} == 7
%{__make} PYTHON=/usr/bin/python docs
%endif

%install
%{__rm} -rf %{buildroot}

%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/doc/en_US/html
%{__cp} -pr docs/en_US/_build/html/* %{buildroot}%{pgadmin4instdir}/doc/en_US/html/

%{__install} -d %{buildroot}%{pgadmin4instdir}/bin
%{__cp} runtime/pgAdmin4 %{buildroot}%{pgadmin4instdir}/bin
chrpath -r "\${ORIGIN}/../venv/lib" %{buildroot}%{pgadmin4instdir}/bin/pgAdmin4

%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/venv
%{__cp} -pR linux-build/venv/* %{buildroot}%{pgadmin4instdir}/venv
patchelf --set-rpath '${ORIGIN}/../lib' %{buildroot}%{pgadmin4instdir}/venv/bin/python%{pyver}

find %{buildroot}%{pgadmin4instdir}/venv -type f | xargs -I{} file {} | grep ELF | cut -f1 -d":" | xargs -I{} chmod -x {}

%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/web
%{__cp} -pR web/* %{buildroot}%{pgadmin4instdir}/web/

# Install Apache sample config file
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__sed} -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' < %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf.sample

# Install Apache config script
%{__install} -d %{buildroot}%{pgadmin4instdir}/bin
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' < %{SOURCE7} > %{buildroot}%{pgadmin4instdir}/bin/%{name}-web-setup.sh

# Install desktop file, and its icon
%{__install} -d -m 755 %{buildroot}%{pgadmin4instdir}/web/pgadmin/static/img/
%{__install} -m 755 runtime/pgAdmin4.ico %{buildroot}%{pgadmin4instdir}/web/pgadmin/static/img/
%{__install} -d %{buildroot}%{_datadir}/applications/
%{__sed} -e 's@PYTHONDIR@%{__ospython}@g' -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' < %{SOURCE4} > %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install QT conf file.
# Directories are different on RHEL 7 and Fedora 24+.
%if 0%{?fedora} > 25 || 0%{?rhel} == 8
# Fedora 24+
%{__install} -d "%{buildroot}%{_sysconfdir}/xdg/pgadmin/"
%{__sed} -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' <%{SOURCE6} > "%{buildroot}%{_sysconfdir}/xdg/pgadmin/%{name}.conf"
%else
# CentOS 7
%{__install} -d "%{buildroot}%{_sysconfdir}/pgadmin/"
%{__sed} -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' <%{SOURCE6} > "%{buildroot}%{_sysconfdir}/pgadmin/%{name}.conf"
%endif

%if %{systemd_enabled}
# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__sed} -e 's@PGADMIN4INSTDIR@%{pgadmin4instdir}@g' -e 's@OSPYTHON@%{__ospython}@g'<%{SOURCE8} > "%{buildroot}%{_unitdir}/%{name}.service"
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf
%endif

cd %{buildroot}%{PYTHON_SITELIB}/%{name}-web
%{__rm} -f %{name}.db
echo "HELP_PATH = '/usr/share/doc/%{name}-docs/en_US/html'" > config_distro.py
# Disable upgrade check in the packages:
echo "UPGRADE_CHECK_ENABLED = False" >> config_distro.py


# Manually invoke the python byte compile macro for each path that needs byte
# compilation. All platforms except RHEL 6:
%if 0%{?rhel} <= 6
/bin/true
%else
find %{buildroot} -iname -type f -a "*.py" -exec -print0 | xargs -0 %{__ospython} -O -m py_compile \
find %{buildroot} -iname -type f -a "*.py" -exec -print0 | xargs -0 %{__ospython}  -m py_compile \
%endif

%clean
%{__rm} -rf %{buildroot}

%post
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

%post -n %{name}-desktop-common
if [ $1 > 1 ] ; then
 %{__ln_s} %{pgadmin4instdir}/runtime/pgAdmin4 %{_bindir}/pgadmin4 >/dev/null 2>&1 || :
fi

%post -n %{name}-desktop-gnome
%if 0%{?fedora} > 25 || 0%{?rhel} == 8
	# Enable the extension. Don't throw an error if it is already enabled.
	gnome-shell-extension-tool -e topicons-plus >/dev/null 2>&1 || :
%endif

%post -n %{name}-web
find %{pgadmin4instdir}/venv/* -type f | xargs -I{} file {} | grep ELF | cut -f1 -d":" | xargs -I{} chmod +x {}

%postun
# Remove symlink only during uninstall
if [ $1 -gt 0 ] ; then
	unlink %{_bindir}/pgadmin4 >/dev/null 2>&1 || :
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
%dir %{PYTHON_SITELIB}/%{name}-web/
%dir %{pgadmin4instdir}/web
%dir %{pgadmin4instdir}/venv
%{pgadmin4instdir}/web/*
%{pgadmin4instdir}/venv/*
%{PYTHON_SITELIB}/%{name}-web/*
%attr(700,root,root) %{pgadmin4instdir}/bin/%{name}-web-setup.sh
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf.sample
%if %{systemd_enabled}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%endif

%files -n %{name}-docs
%defattr(-,root,root,-)
%doc	%{pgadmin4instdir}/doc/en_US/html/

%files -n %{name}-desktop-common
%defattr(-,root,root,-)
%{pgadmin4instdir}/bin/pgAdmin4
%{_datadir}/applications/%{name}.desktop
%if 0%{?fedora} > 25 || 0%{?rhel} == 8
%{_sysconfdir}/xdg/pgadmin/%{name}.conf
%else
%{_sysconfdir}/pgadmin/%{name}.conf
%endif

%files -n %{name}-desktop-gnome
%defattr(-,root,root,-)

%changelog
* Thu Apr 18 2019 - Devrim Gündüz <devrim@gunduz.org> 4.5-1
- Update to 4.5
- Use virtualenv for the dependencies, the package will be easier
  to maintain.

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
