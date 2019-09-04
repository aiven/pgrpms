%global sname	flask-paranoid

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
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

Version:	0.2
Release:	1%{?dist}.1
Summary:	Simple user session protection
License:	MIT
URL:		https://github.com/miguelgrinberg/%{sname}
Source0:	https://github.com/miguelgrinberg/%{sname}/archive/v%{version}.tar.gz
BuildArch:	noarch

%description
Simple user session protection.

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname}
BuildRequires:	python34-devel python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/Flask_Paranoid* %{buildroot}%{python3_sitelib}/flask_paranoid %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/Flask_Paranoid* %{buildroot}%{python2_sitelib}/flask_paranoid %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README.md
%else
%license LICENSE
%doc README.md
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Flask_Paranoid*.egg-info/
%dir %{pgadmin4py3instdir}/flask_paranoid
%{pgadmin4py3instdir}/flask_paranoid/*
%else
%{pgadmin4py2instdir}/Flask_Paranoid*.egg-info/
%dir %{pgadmin4py2instdir}/flask_paranoid
%{pgadmin4py2instdir}/flask_paranoid/*
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2-1
- Update to 0.2

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-2
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Sep 6 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-1
- Initial packaging to satisfy pgadmin4 2.0 dependencies
