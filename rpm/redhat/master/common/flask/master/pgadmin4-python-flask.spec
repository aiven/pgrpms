%global sname flask
%global srcname Flask

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		pgadmin4-python3-%{sname}
Version:	1.0.2
Release:	3%{?dist}
Epoch:		1
Summary:	A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
License:	BSD
URL:		http://flask.pocoo.org/
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
BuildRequires:	python3-jinja2 python3-werkzeug python3-itsdangerous
BuildRequires:	python3-click
Requires:	python3-werkzeug python3-itsdangerous python3-click
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-python3-jinja2 pgadmin4-python3-werkzeug
BuildRequires:	pgadmin4-python3-itsdangerous python36-click
Requires:	pgadmin4-python3-jinja2	pgadmin4-python3-werkzeug
Requires:	pgadmin4-python3-itsdangerous python36-click
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
CFLAGS="%{optflags}" %{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{srcname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

# Remove binary, we don't need it in pgadmin4 packaging.
%{__rm} %{buildroot}%{_bindir}/%{sname}


%files
%license LICENSE
%doc CHANGES.rst README.rst
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Wed Apr 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.2-3
- Fix RHEL 7 dependencies, per Talha.

* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.2-2
- Switch to PY3 on RHEL 7

* Thu May 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.2-1
- Update to 1.0.2

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1:0.12.4-1
- Update to 0.12.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:0.12.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1:0.12.2-1
- Update to 0.12.2

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-9
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-6
- Move the components under pgadmin web directory, per #2332.
- Remove flask binary, we don't need it in pgadmin4 packaging.

* Mon Oct 10 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-5
- Fix unmet dependencies issue in spec file. Fixes #1738.
  Patch by Martin Collins.
- Fix rpmlint warnings (convert spaces to tabs)
- Fix PY2 dependencies.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.11.1-4
- Initial packaging for PostgreSQL YUM repo, to satisfy pgadmin4 dependency.
  Previous packaging had some conflicts.
