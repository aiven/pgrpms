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

%global sname blinker

%if 0%{?with_python3}
Name:           pgadmin4-python3-%{sname}
%else
Name:           pgadmin4-python-%{sname}
%endif
Version:        1.4
Release:        2%{?dist}
Summary:        Fast, simple object-to-object and broadcast signaling

Group:          Development/Libraries
License:        MIT
URL:            http://discorporate.us/projects/Blinker/
Source0:        https://pypi.python.org/packages/source/b/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%else
BuildRequires:	python2-devel
%endif
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Blinker provides a fast dispatching system that allows any number
of interested parties to subscribe to events, or "signals".

%prep
%setup -q -n %{sname}-%{version}

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
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files

%if 0%{?with_python3}
%files -n pgadmin4-python3-blinker
%doc docs/ CHANGES LICENSE README.md
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%doc docs/ CHANGES LICENSE README.md
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 1.4-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Sun Oct 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependencies.
