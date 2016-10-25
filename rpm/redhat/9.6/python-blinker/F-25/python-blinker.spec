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

%global mod_name blinker

Name:           python-blinker
Version:        1.4
Release:        1%{?dist}
Summary:        Fast, simple object-to-object and broadcast signaling

Group:          Development/Libraries
License:        MIT
URL:            http://discorporate.us/projects/Blinker/
Source0:        http://pypi.python.org/packages/source/b/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Blinker provides a fast dispatching system that allows any number
of interested parties to subscribe to events, or "signals".

%if 0%{?with_python3}
%package -n python3-blinker
Summary:        Fast, simple object-to-object and broadcast signaling

%description -n python3-blinker
Blinker provides a fast dispatching system that allows any number
of interested parties to subscribe to events, or "signals".
%endif

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%{__ospython2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}

 
%files
%doc docs/ CHANGES LICENSE README.md
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{mod_name}

%if 0%{?with_python3}
%files -n python3-blinker
%doc docs/ CHANGES LICENSE README.md
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{mod_name}
%endif


%changelog
* Sun Oct 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependencies.
