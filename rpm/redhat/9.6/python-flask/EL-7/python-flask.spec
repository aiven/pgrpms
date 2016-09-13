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

%global modname flask
%global srcname Flask

Name:           python-%{modname}
Version:        0.11.1
Release:        4%{?dist}
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

License:        BSD
URL:            http://flask.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
Group:          Development/Languages

%description -n python3-%{modname}
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.
%endif # with_python3

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-jinja2
BuildRequires:  python3-werkzeug
BuildRequires:  python3-itsdangerous
BuildRequires:  python3-click
Requires:       python3-jinja2
Requires:       python3-werkzeug
Requires:       python3-itsdangerous
Requires:       python3-click
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python-jinja2
BuildRequires:  python-werkzeug
BuildRequires:  python-itsdangerous
BuildRequires:  python-click
Requires:       python-jinja2
Requires:       python-werkzeug
Requires:       python-itsdangerous
Requires:       python-click
%endif

%prep
%setup -q -n %{srcname}-%{version}
%{__rm} -vf examples/flaskr/.gitignore

%build
CFLAGS="%{optflags}" %{__ospython2} setup.py build

%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
%endif # with_python3

%{__ospython2} setup.py install --skip-build --root %{buildroot}


%files
%{_bindir}/%{modname}
%doc CHANGES README LICENSE
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/%{modname}/

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{modname}/
%endif

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-4
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
  Previous packaging had some conflicts.
