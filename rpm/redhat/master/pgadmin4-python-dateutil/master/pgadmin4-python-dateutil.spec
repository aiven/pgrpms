%global sname dateutil
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

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

Name:		pgadmin4-python-%{sname}
Version:	2.5.3
Release:	4%{?dist}
Epoch:		1
Summary:	Powerful extensions to the standard datetime module
License:	Python
URL:		https://github.com/dateutil/dateutil
Source0:	https://github.com/dateutil/dateutil/archive/%{version}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python-sphinx

%{?python_provide:%python_provide python-%{sname}}
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%else
BuildRequires:	python2-devel
%endif
BuildRequires:	python-six
BuildRequires:	python-setuptools
Requires:	tzdata
Requires:	python-six

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%package doc
Summary:	API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n %{sname}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%if 0%{?rhel} && 0%{?rhel} <= 6
:
%else
%{__make} -C docs html
%endif
%{__ospython2} setup.py build

%install
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/python_%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc NEWS README.rst
%{pgadmin4py2instdir}/python_%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%files doc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%doc docs/_build/html
%endif

%changelog
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

