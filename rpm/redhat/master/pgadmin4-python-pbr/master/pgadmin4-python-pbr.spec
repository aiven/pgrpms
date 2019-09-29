%global sname pbr

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
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

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	3.1.1
Release:	1%{?dist}.1
Summary:	Python Build Reasonableness

License:	ASL 2.0
URL:		https://pypi.python.org/pypi/pbr
Source0:	https://files.pythonhosted.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%description
PBR is a library that injects some useful and sensible default behaviors into
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18
different projects each with at least 3 active branches, it seems like a good
time to make that code into a proper re-usable library.
%{?python_provide:%python_provide python2-%{sname}}

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%build
export SKIP_PIP_INSTALL=1
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
%{__rm} -rf %{buildroot}%{python3_sitelib}/pbr/tests
%else
%{__rm} -rf %{buildroot}%{python2_sitelib}/pbr/tests
%endif

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

# Remove binary, we don't need it in this package:
%{__rm} %{buildroot}%{_bindir}/pbr

%files
%doc README.rst LICENSE
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Sat Apr 7 2018 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-8
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Sat May 6 2017 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-7
- Remove binary, we don't need it in this spec file.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-6
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-5
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.

