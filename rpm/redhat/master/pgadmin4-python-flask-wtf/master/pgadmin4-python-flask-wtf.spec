%global build_timestamp %(date +"%Y%m%d")
%global sname	flask-wtf

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.14.3
Release:	1%{?dist}
Summary:	Simple integration of Flask and WTForms

License:	BSD
URL:		https://github.com/lepture/%{sname}
Source0:	https://github.com/lepture/%{sname}/archive/v%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 27
BuildRequires:  python3-devel python3-setuptools python3-wtforms > 1.0
BuildRequires:	python3-flask-babel python3-flask python3-nose
%endif

%if 0%{?rhel} == 7
BuildRequires:  python2-devel python-setuptools pgadmin4-python-wtforms
BuildRequires:	pgadmin4-python-flask-babel pgadmin4-python-flask
BuildRequires:	python-nose
%endif

%if 0%{?rhel} == 8
BuildRequires:  python3-devel python3-setuptools pgadmin4-python3-wtforms > 1.0
BuildRequires:	pgadmin4-python3-flask-babel python3-flask python3-nose
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif

%description
Flask-WTF offers simple integration with WTForms. This integration
includes optional CSRF handling for greater security.

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -f docs/index.rst.orig

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_wtf %{buildroot}%{python3_sitelib}/Flask_WTF-%{version}.dev%{build_timestamp}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_wtf %{buildroot}%{python2_sitelib}/Flask_WTF-%{version}.dev_%{build_timestamp}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc docs/ LICENSE
%else
%license LICENSE
%doc docs/
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*Flask_WTF*.egg-info
%{pgadmin4py3instdir}/flask_wtf
%else
%{pgadmin4py2instdir}/*Flask_WTF*.egg-info
%{pgadmin4py2instdir}/flask_wtf
%endif

%changelog
* Fri Feb 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.14.3-1
- Update to 0.14.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.14.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.14.2-1
- Update to 0.14.2

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0.12-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.12-2
- Move the components under pgadmin web directory, per #2332.

* Sun Sep 11 2016 Devrim Gündüz <devrim@gunduz.org> - 0.12-1
- Update to 0.12, to satisfy pgadmin4 dependency.

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

