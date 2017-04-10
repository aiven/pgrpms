%global mod_name WTForms
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

Name:		python-wtforms
Version:	2.1
Release:	1%{?dist}
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

%if 0%{?with_python3}
%package -n python3-wtforms
Summary:	Forms validation and rendering library for python

%description -n python3-wtforms
With wtforms, your form field HTML can be generated for you.
This allows you to maintain separation of code and presentation,
and keep those messy parameters out of your python code.
%endif

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
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}

%{__mkdir} -p %{buildroot}/%{_datadir}
%{__mv} %{buildroot}/%{python_sitelib}/wtforms/locale %{buildroot}%{_datadir}
find %{buildroot}%{_datadir}/locale -name '*.po*' -delete

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf %{buildroot}/%{python3_sitelib}/wtforms/locale
%endif

%find_lang wtforms

%files -f wtforms.lang
%doc docs/ LICENSE.txt PKG-INFO
%{python_sitelib}/*.egg-info
%{python_sitelib}/wtforms/

%if 0%{?with_python3}
%files -n python3-wtforms -f wtforms.lang
%doc docs/ LICENSE.txt PKG-INFO
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/wtforms/
%endif

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
