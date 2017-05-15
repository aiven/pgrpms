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

%global sname mimeparse

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/


%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	1.5.2
Release:	2%{?dist}
Summary:	Python module for parsing mime-type names
Group:		Development/Languages
License:	MIT
URL:		https://pypi.python.org/pypi/python-mimeparse
Source0:	https://files.pythonhosted.org/packages/source/p/python-%{sname}/python-%{sname}-%{version}.tar.gz
BuildArch:	noarch
%if 0%{?with_python3}
BuildRequires:	python3-devel
%else
BuildRequires:	python2-devel
Provides:	python2-mimeparse
%endif # if with_python3

%description
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.

%prep
%setup -q -n python-%{sname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
popd
%else
CFLAGS="%{optflags}" %{__ospython2} setup.py build
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname}.py %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}%{python3_sitelib}/python_%{sname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}.py %{buildroot}%{python2_sitelib}/python_%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3

%files
%doc README.md
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/__pycache__/%{sname}*
%{pgadmin4py3instdir}/%{sname}*
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}*
%ghost %{python2_sitelib}/%{sname}.pyc
%endif

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Wed Nov 02 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-1
- Initial version
