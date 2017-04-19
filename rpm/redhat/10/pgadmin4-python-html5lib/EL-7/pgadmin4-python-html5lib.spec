%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%endif


%global sname html5lib

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Summary:	A python based HTML parser/tokenizer
Version:	1.0b3
Release:	1%{?dist}
Epoch:		1
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{sname}

Source0:	https://pypi.python.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
%if 0%{?with_python3}
Requires:	python3-six
%else
Requires:	python-six
%endif
%if 0%{?with_python3}
BuildRequires:	python3-setuptools python3-devel
BuildRequires:	python3-six python3-nose
%else
BuildRequires:	python-setuptools python2-devel
BuildRequires:	python-six python-nose
%endif

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5
specification for maximum compatibility with major desktop web browsers.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc CHANGES.rst README.rst LICENSE
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Wed Apr 19 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.0b3
- Update to 1.0b3, and add to all distros, so add PY3 packages as well.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.999-6
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.999-5
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
