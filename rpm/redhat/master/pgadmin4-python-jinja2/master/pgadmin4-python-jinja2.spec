%global srcname Jinja2
%global sname jinja2

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 0

Name:		pgadmin4-python3-%{sname}
Version:	2.8
Release:	10%{?dist}
Summary:	General purpose template engine
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	https://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
BuildRequires:	python3-markupsafe
Requires:	python3-babel >= 0.8 python3-markupsafe
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-python3-markupsafe
Requires:	pgadmin4-python3-babel >= 0.8 pgadmin4-python3-markupsafe
%endif

%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.

%prep
%setup -qc -n %{srcname}-%{version}

pushd %{srcname}-%{version}
# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete
# fix EOL
sed -i 's|\r$||g' LICENSE
popd

%build
pushd %{srcname}-%{version}
%{__ospython} setup.py build

# for now, we build docs using Python 2.x and use that for both
# packages.
%if 0%{?with_docs}
make -C docs html PYTHONPATH=${pwd}
%endif
popd

%install
pushd %{srcname}-%{version}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# remove hidden file
%{__rm} -rf docs/_build/html/.buildinfo

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{srcname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd

%files
%license %{srcname}-%{version}/LICENSE
%doc %{srcname}-%{version}/CHANGES
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%if 0%{?rhel} && 0%{?rhel} > 6
%exclude %{python2_sitelib}/jinja2/_debugsupport.c
%endif

%changelog
* Wed Mar 4 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8-10
- Switch to PY3 on RHEL 7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8-9.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8-9
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 2.8-8
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.8-7
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
