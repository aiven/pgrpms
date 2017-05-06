%global sname pbr
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		pgadmin4-python-%{sname}
Version:	1.8.1
Release:	7%{?dist}
Summary:	Python Build Reasonableness

License:	ASL 2.0
URL:		http://pypi.python.org/pypi/pbr
Source0:	http://pypi.python.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%description
PBR is a library that injects some useful and sensible default behaviors into
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18
different projects each with at least 3 active branches, it seems like a good
time to make that code into a proper re-usable library.
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:	python2-devel

%if 0%{?do_test} == 1
BuildRequires:	python-coverage
BuildRequires:	python-hacking
BuildRequires:	python-mock
BuildRequires:	python-testrepository
BuildRequires:	python-testresources
BuildRequires:	python-testscenarios
BuildRequires:	gcc
BuildRequires:	git
BuildRequires:	gnupg
%endif

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%build
export SKIP_PIP_INSTALL=1
%{__ospython2} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython2} setup.py install --skip-build --root %{buildroot}
%{__rm} -rf %{buildroot}%{python_sitelib}/pbr/tests

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python_sitelib}/%{sname} %{buildroot}%{python_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
# Remove binary, we don't need it in this package:
%{__rm} %{buildroot}%{_bindir}/pbr

%files
%doc README.rst LICENSE
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Sat May 6 2017 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-7
- Remove binary, we don't need it in this spec file.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-6
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon Sep 12 2016 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-5
- Initial packaging for PostgreSQL YUM repository, for pgadmin4 dependency.
  Spec file is Fedora rawhide spec as of today.

