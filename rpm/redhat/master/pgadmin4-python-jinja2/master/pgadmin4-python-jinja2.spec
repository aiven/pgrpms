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
%global mod_name Jinja2
%global sname jinja2

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 1

Name:		pgadmin4-python-%{sname}
Version:	2.8
Release:	8%{?dist}
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz

BuildArch:	noarch
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytest
%endif
%else
BuildRequires:	python2-devel pytest
%endif
BuildRequires:	python-setuptools python-markupsafe
%if 0%{?with_docs}
BuildRequires:	python-sphinx
%endif # with_docs
Requires:	python-babel >= 0.8 python-markupsafe python-setuptools

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
%setup -qc -n %{mod_name}-%{version}
%{__mv} %{mod_name}-%{version} python2

pushd python2

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete

# fix EOL
sed -i 's|\r$||g' LICENSE

popd

%build
pushd python2
%{__python} setup.py build

# for now, we build docs using Python 2.x and use that for both
# packages.
%if 0%{?with_docs}
make -C docs html PYTHONPATH=$(pwd)
%endif # with_docs
popd

%install
pushd python2
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# remove hidden file
%{__rm} -rf docs/_build/html/.buildinfo
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{mod_name}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
popd

%files
%doc python2/AUTHORS
%doc python2/CHANGES
%doc python2/LICENSE
%if 0%{?with_docs}
%doc python2/docs/_build/html
%endif # with_docs
%doc python2/ext
%doc python2/examples
%{pgadmin4py2instdir}/*%{mod_name}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%if 0%{?rhel} && 0%{?rhel} > 6
%exclude %{python2_sitelib}/jinja2/_debugsupport.c
%endif

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 2.8-8
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.8-7
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
