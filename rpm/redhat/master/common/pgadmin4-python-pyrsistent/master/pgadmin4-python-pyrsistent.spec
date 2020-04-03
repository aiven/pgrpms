%global	sname	pyrsistent

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
Summary:	Persistent/Functional/Immutable data structures
Version:	0.14.2
Release:	1%{?dist}.2
License:	MIT
Source0:	https://github.com/tobgu/%{sname}/archive/v%{version}.tar.gz
URL:		http://github.com/tobgu/%{sname}/

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
Requires:	python3-six
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
Requires:	python-six
%endif

%description
%{sname} is a number of persistent collections (by some referred to
as functional data structures). Persistent in the sense that they are
immutable.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/__pycache__/*%{sname}* %{buildroot}%{python3_sitearch}/_%{sname}_version.py %{buildroot}%{python3_sitearch}/pvectorc.cpython*  %{buildroot}%{python3_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname}* %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/_%{sname}_version.py* %{buildroot}%{python2_sitearch}/pvectorc.* %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.rst
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%dir %{pgadmin4py3instdir}/%{sname}
%{pgadmin4py3instdir}/%{sname}/*
%{pgadmin4py3instdir}/__pycache__/*%{sname}*
%{pgadmin4py3instdir}/_%{sname}*
%{pgadmin4py3instdir}/pvectorc*.so
%else
%dir %{pgadmin4py2instdir}/%{sname}
%{pgadmin4py2instdir}/%{sname}/*
%{pgadmin4py2instdir}/_%{sname}*
%{pgadmin4py2instdir}/%{sname}*egg-info/
%{pgadmin4py2instdir}/pvectorc*.so
%endif

%changelog
* Wed Dec 19 2018 John K. Harvey <john.harvey@crunchydata.com> - 0.14.2-1.2
- Fix dist macro

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.14.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.14.2-1
- Update to 0.14.2

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0.11.13-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> 0.11.13-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-2
- Fix packaging errors, that would own /usr/lib64 or so.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.


