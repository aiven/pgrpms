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

%global srcname mimeparse

Name:           python-%{srcname}
Version:        1.5.2
Release:        1%{?dist}
Summary:        Python module for parsing mime-type names
Group:          Development/Languages
License:        MIT
URL:            https://pypi.python.org/pypi/python-mimeparse
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3
Provides:       python2-mimeparse

%description
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Python module for parsing mime-type names
Group:          Development/Languages

%description -n python3-%{srcname}
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.
%endif # with_python3

%prep
%setup -q -n %{name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__ospython2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__ospython3} setup.py build
popd
%endif # with_python3

%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__ospython2} setup.py install --skip-build --root %{buildroot}

%files
%doc README.md
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.md
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Wed Nov 02 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-1
- Initial version
