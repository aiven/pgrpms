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

%global sname flask
%global srcname Flask
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.11.1
Release:	6%{?dist}
Epoch:		1
Summary:	A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

License:	BSD
URL:		http://flask.pocoo.org/
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{sname}}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-pytest
BuildRequires:	python3-jinja2
BuildRequires:	python3-werkzeug
BuildRequires:	python3-itsdangerous
BuildRequires:	python3-click
Requires:	python3-jinja2
Requires:	python3-werkzeug
Requires:	python3-itsdangerous
Requires:	python3-click
%else
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	pytest
BuildRequires:	pgadmin4-python-jinja2
BuildRequires:	pgadmin4-python-werkzeug
BuildRequires:	pgadmin4-python-itsdangerous
BuildRequires:	python-click
Requires:	pgadmin4-python-jinja2
Requires:	pgadmin4-python-werkzeug
Requires:	pgadmin4-python-itsdangerous
Requires:	python-click
%endif

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.

%prep
%setup -q -n %{srcname}-%{version}
%{__rm} -vf examples/flaskr/.gitignore

%build
%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
%else
CFLAGS="%{optflags}" %{__ospython2} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{srcname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{srcname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3


%files
%{_bindir}/%{sname}
%doc CHANGES README LICENSE
%if 0%{?with_python3}
%license LICENSE
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%else
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%endif

%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-6
- Move the components under pgadmin web directory, per #2332.

* Mon Oct 10 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-5
- Fix unmet dependencies issue in spec file. Fixes #1738.
  Patch by Martin Collins.
- Fix rpmlint warnings (convert spaces to tabs)
- Fix PY2 dependencies.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-4
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
  Previous packaging had some conflicts.
