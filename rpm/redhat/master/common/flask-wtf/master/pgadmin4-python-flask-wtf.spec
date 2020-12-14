%global sname	flask-wtf

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-python3-%{sname}
Version:	0.14.3
Release:	2%{?dist}
Summary:	Simple integration of Flask and WTForms

License:	BSD
URL:		https://github.com/lepture/%{sname}
Source0:	https://github.com/lepture/%{sname}/archive/%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 27
BuildRequires:	python3-devel python3-setuptools python3-wtforms > 1.0
BuildRequires:	python3-flask-babel python3-flask python3-nose
%endif

%if 0%{?rhel} >= 7
BuildRequires:	python3-devel python3-setuptools pgadmin4-python3-wtforms > 1.0
BuildRequires:	pgadmin4-python3-flask-babel
%endif

%if 0%{?rhel} == 7
BuildRequires:	python36-nose2 pgadmin4-python3-flask
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-nose python3-flask
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
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_wtf %{buildroot}%{python3_sitelib}/Flask_WTF-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%doc docs/
%{pgadmin4py3instdir}/*Flask_WTF*.egg-info
%{pgadmin4py3instdir}/flask_wtf

%changelog
* Mon Dec 14 2020 Devrim Gündüz <devrim@gunduz.org> - 0.14.3-2
- Make sure that release number matches changelog version.

* Fri Feb 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.14.3-1
- Update to 0.14.3
- Switch to PY3 on RHEL 7, too.

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

