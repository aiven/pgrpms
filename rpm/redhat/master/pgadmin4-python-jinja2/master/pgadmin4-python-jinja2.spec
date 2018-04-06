%global srcname Jinja2
%global sname jinja2

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

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 1

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	2.8
Release:	9%{?dist}
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	https://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
%if 0%{?rhel} == 6
Patch0:		pgadmin4-python-jinja2-rhel6-sphinx.patch
%endif
BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-pytest python3-setuptools
BuildRequires:	python3-markupsafe python3-sphinx
Requires:	python3-babel >= 0.8 python3-markupsafe python3-setuptools
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-pytest python34-setuptools
BuildRequires:	python34-markupsafe python-sphinx10
Requires:	python-babel >= 0.8 python34-markupsafe python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python-devel python-pytest python-setuptools
BuildRequires:	python-markupsafe python-sphinx
Requires:	python-babel >= 0.8 python-markupsafe python-setuptools
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytest
%endif
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
%if 0%{?rhel} == 6
%patch0 -p0
%endif

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
%endif # with_docs
popd

%install
pushd %{srcname}-%{version}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# remove hidden file
%{__rm} -rf docs/_build/html/.buildinfo

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{srcname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{srcname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3
popd

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{srcname}-%{version}/LICENSE %{srcname}-%{version}/CHANGES
%else
%license %{srcname}-%{version}/LICENSE
%doc %{srcname}-%{version}/CHANGES
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{srcname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif
%if 0%{?with_docs}
%doc %{srcname}-%{version}/docs/_build/html
%endif # with_docs

%if 0%{?rhel} && 0%{?rhel} > 6
%exclude %{python2_sitelib}/jinja2/_debugsupport.c
%endif

%changelog
* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8-9
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 2.8-8
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.8-7
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
