%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global mod_name Flask-WTF
%global sname	flask-wtf
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.12
Release:	2%{?dist}
Summary:	Simple integration of Flask and WTForms

Group:		Development/Libraries
License:	BSD
URL:		https://github.com/lepture/flask-wtf
Source0:	http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:	noarch
%if 0%{?with_python3}
#FIXME: Add pgadmin4- prefixes where necessary
BuildRequires:	python3-devel
BuildRequires:	python3-wtforms > 1.0
BuildRequires:	python3-setuptools
BuildRequires:	python3-flask
BuildRequires:	python3-nose
%else
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%else
BuildRequires:	python2-devel
%endif
BuildRequires:	pgadmin4-python-wtforms > 1.0
BuildRequires:	python-setuptools
BuildRequires:	pgadmin4-python-flask
BuildRequires:	python-nose
BuildRequires:	pgadmin4-python-flask-babel
%endif

%if 0%{?with_python3}
Requires:	pgadmin4-python3-wtforms > 1.0
%else
Requires:	pgadmin4-python-wtforms > 1.0
%endif

%description
Flask-WTF offers simple integration with WTForms. This integration
includes optional CSRF handling for greater security.

%prep
%setup -q -n %{mod_name}-%{version}
%{__rm} -f docs/index.rst.orig

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_wtf %{buildroot}%{python3_sitelib}/Flask_WTF-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_wtf %{buildroot}%{python2_sitelib}/Flask_WTF-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%doc docs/ LICENSE PKG-INFO
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*Flask_WTF*.egg-info
%{pgadmin4py3instdir}/flask_wtf
%else
%{pgadmin4py2instdir}/*Flask_WTF*.egg-info
%{pgadmin4py2instdir}/flask_wtf
%endif

%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.12-2
- Move the components under pgadmin web directory, per #2332.

* Sun Sep 11 2016 Devrim Gündüz <devrim@gunduz.org> - 0.12-1
- Update to 0.12, to satisfy pgadmin4 dependency.

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

