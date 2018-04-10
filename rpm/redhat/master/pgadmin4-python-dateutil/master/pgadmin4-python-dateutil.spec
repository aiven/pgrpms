%global sname dateutil

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
%if 0%{?rhel} == 6
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
Version:	2.7.2
Release:	1%{?dist}
Epoch:		1
Summary:	Powerful extensions to the standard datetime module
License:	Python
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://files.pythonhosted.org/packages/c5/39/4da7c2dbc4f023fba5fb2325febcadf0d0ce0efdc8bd12083a0f65d20653/python-%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-sphinx python3-devel python3-setuptools
Requires:	python3-six
%endif

%if 0%{?rhel} == 6
BuildRequires:	python-sphinx10 python34-devel python34-setuptools
Requires:	python34-six
%endif

%if 0%{?rhel} == 7
Obsoletes:	pgadmin4-python-%{sname} < %{version}
BuildRequires:	python-sphinx python2-devel python-six python-setuptools
Requires:	python-six
%endif

%{?python_provide:%python_provide python-%{sname}}
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif


%description
The %{sname} module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%package doc
Summary:	API documentation for python-%{sname}
%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n python-%{sname}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%if 0%{?rhel} && 0%{?rhel} <= 6
:
%else
%{__make} -C docs html
%endif
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/python_%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/python_%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc NEWS README.rst
%if 0%{?with_python3}
%{pgadmin4py3instdir}/python_%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/python_%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%files doc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%doc docs/_build/html
%endif

%changelog
* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1:2.7.2-1
- Update to 2.7.2

* Thu Apr 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-5
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-4
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon Sep 26 2016 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-3
- Fix spec file, description part, package part, etc. Fixes #1706.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-2
- Change PY2 package name.

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

