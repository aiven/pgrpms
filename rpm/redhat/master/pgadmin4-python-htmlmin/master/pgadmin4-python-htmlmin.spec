%global sname htmlmin
%global desc A configurable HTML Minifier with safety features.

%if 0%{?rhel} && 0%{?rhel} <= 6
%global with_docs 0
%else
%global with_docs 1
%endif

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
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
Version:	0.1.12
Release:	1%{?dist}.1
Summary:	HTML Minifier

License:	BSD
URL:		https://pypi.python.org/pypi/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif

%description
%{desc}

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -rf *.egg-info

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%if 0%{?with_python3}
%files -n pgadmin4-python3-%{sname}
%else
%files -n pgadmin4-python-%{sname}
%endif
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README.rst
%else
%license LICENSE
%doc README.rst
%endif
%{_bindir}/htmlmin
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.12-1.1
- Rebuild against PostgreSQL 11.0

* Mon Apr 16 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.12-1
- Update to 0.1.12

* Sat Apr 7 2018 Devrim Gündüz <devrim@gunduz.org> -  0.1.10-8.gitcc611c3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-6.gitcc611c3
- Move the components under pgadmin web directory, per #2332.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-6.gitcc611c3
- Add a macro for docs, and enable in on RHEL 7 and onwards.

* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-5.gitcc611c3
- Initial packaging for PostgreSQL YUM repo, based on Fedora rawhide spec.

