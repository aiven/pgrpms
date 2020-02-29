%global sname dateutil

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	2.8.0
Release:	2%{?dist}
Epoch:		1
Summary:	Powerful extensions to the standard datetime module
License:	Python
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://files.pythonhosted.org/packages/ad/99/5b2e99737edeb28c71bcbec5b5dda19d0d9ef3ca3e92e3e925e7c0bb364c/python-dateutil-2.8.0.tar.gz

BuildArch:	noarch

BuildRequires:	python3-sphinx python3-devel python3-setuptools

%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
Requires:	python3-six
%endif

%if 0%{?rhel} == 7
Obsoletes:	pgadmin4-python-%{sname} < %{version}
BuildRequires:	pgadmin4-python3-six
Requires:	pgadmin4-python3-six
%endif

%{?python_provide:%python_provide python-%{sname}}

%description
The %{sname} module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 3.

%package doc
Summary:	API documentation for python-%{sname}
%description doc
This package contains %{summary}.

%prep
%autosetup -n python-%{sname}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__make} -C docs html
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/python_%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%license LICENSE
%doc NEWS README.rst
%{pgadmin4py3instdir}/python_%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%files doc
%license LICENSE
%doc docs/_build/html

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.0-2
- Switch to PY3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.0-1
- Update to 2.8.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:2.7.2-1.1
- Rebuild against PostgreSQL 11.0

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

