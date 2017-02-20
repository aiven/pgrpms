%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

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
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
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

