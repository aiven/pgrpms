%global modname dateutil

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}

Name:		python-%{modname}
Version:	2.5.3
Release:	2%{?dist}
Epoch:		1
Summary:	Powerful extensions to the standard datetime module

Group:		Development/Languages
License:	Python
URL:		https://github.com/dateutil/dateutil
Source0:	https://github.com/dateutil/dateutil/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python-sphinx

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%{?python_provide:%python_provide python-%{modname}}
BuildRequires:	python2-devel
%if 0%{?with_python3}
BuildRequires:	python3-six
BuildRequires:	python3-setuptools
%else
BuildRequires:	python-six
BuildRequires:	python-setuptools
%endif
Requires:	tzdata
Requires:	python2-six

%description -n python-%{modname}
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:	Powerful extensions to the standard datetime module
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:	python3-devel
BuildRequires:	python3-six
BuildRequires:	python3-setuptools
Requires:	tzdata
Requires:	python3-six

%description -n python3-dateutil
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 3.
%endif #with py3

%package doc
Summary:	API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n %{modname}-%{version}
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

# If Py3:
%if 0%{?with_python3}
%files -n python3-%{modname}
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
#endif for license tag
%endif
%doc NEWS README.rst
%{python_sitelib}/%{modname}/
%{python_sitelib}/*.egg-info
%else
#if Python 2:
%files -n python-%{modname}
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc NEWS README.rst
%{python_sitelib}/%{modname}/
%{python_sitelib}/*.egg-info
%endif

%files doc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%doc docs/_build/html
%endif

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-2
- Change PY2 package name.

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 1:2.5.3-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

