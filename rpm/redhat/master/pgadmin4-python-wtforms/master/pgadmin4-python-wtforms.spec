%global mod_name WTForms
%global sname wtforms

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
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	2.1
Release:	2%{?dist}
Summary:	Forms validation and rendering library for python

Group:		Development/Libraries
License:	BSD
URL:		http://wtforms.simplecodes.com/
Source0:	http://pypi.python.org/packages/source/W/%{mod_name}/%{mod_name}-%{version}.zip

BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif

%description
With wtforms, your form field HTML can be generated for you.
This allows you to maintain separation of code and presentation,
and keep those messy parameters out of your python code.

%prep
%setup -q -n %{mod_name}-%{version}
sed -i "s|\r||g" docs/html/_sources/index.txt
sed -i "s|\r||g" docs/conf.py
sed -i "s|\r||g" docs/Makefile
sed -i "s|\r||g" docs/index.rst
sed -i "s|\r||g" docs/html/_static/jquery.js
%{__rm} -f docs/html/.buildinfo

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py build
popd
%else
%{__ospython2} setup.py build
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{mod_name}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{mod_name}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?with_python3}
%doc docs/ LICENSE.txt PKG-INFO
%{pgadmin4py3instdir}/*%{mod_name}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%doc docs/ LICENSE.txt PKG-INFO
%{pgadmin4py2instdir}/*%{mod_name}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
