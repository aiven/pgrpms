%global mod_name Flask-WTF
%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%else
%{!?with_python3:%global with_python3 0}
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2	%{__python}
%global python2_sitelib %{python_sitelib}
%endif

Name:		python-flask-wtf
Version:	0.12
Release:	1%{?dist}
Summary:	Simple integration of Flask and WTForms

Group:		Development/Libraries
License:	BSD
URL:		https://github.com/lepture/flask-wtf
Source0:	http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-wtforms > 1.0
BuildRequires:	python-setuptools
BuildRequires:	python-flask
BuildRequires:	python-nose
BuildRequires:	python-flask-babel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-wtforms > 1.0
BuildRequires:	python3-setuptools
BuildRequires:	python3-flask
BuildRequires:	python3-nose
%endif

Requires:	python-wtforms > 1.0
%if 0%{?with_python3}
Requires:	python-wtforms > 1.0
%endif

%description
Flask-WTF offers simple integration with WTForms. This integration
includes optional CSRF handling for greater security.

%if 0%{?with_python3}
%package -n python3-flask-wtf
Summary:	Simple integration of Flask and WTForms

%description -n python3-flask-wtf
Flask-WTF offers simple integration with WTForms. This integration
includes optional CSRF handling for greater security.
%endif

%prep
%setup -q -n %{mod_name}-%{version}
rm -f docs/index.rst.orig

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%files
%doc docs/ LICENSE PKG-INFO
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/flask_wtf/

%if 0%{?with_python3}
%files -n python3-flask-wtf
%doc docs/ LICENSE PKG-INFO
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_wtf/
%endif

%changelog
* Sun Sep 11 2016 Devrim Gündüz <devrim@gunduz.org> - 0.12-1
- Update to 0.12, to satisfy pgadmin4 dependency.

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

