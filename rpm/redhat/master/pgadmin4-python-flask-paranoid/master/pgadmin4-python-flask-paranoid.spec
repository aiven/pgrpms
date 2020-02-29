%global sname	flask-paranoid

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.2
Release:	2%{?dist}
Summary:	Simple user session protection
License:	MIT
URL:		https://github.com/miguelgrinberg/%{sname}
Source0:	https://github.com/miguelgrinberg/%{sname}/archive/v%{version}.tar.gz
BuildArch:	noarch

%description
Simple user session protection.

BuildRequires:	python3-devel python3-setuptools

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/Flask_Paranoid* %{buildroot}%{python3_sitelib}/flask_paranoid %{buildroot}/%{pgadmin4py3instdir}

%files
%license LICENSE
%doc README.md
%{pgadmin4py3instdir}/Flask_Paranoid*.egg-info/
%dir %{pgadmin4py3instdir}/flask_paranoid
%{pgadmin4py3instdir}/flask_paranoid/*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.2-2
- Switch to PY3 on RHEL 7.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.2-1
- Update to 0.2

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-2
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Sep 6 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-1
- Initial packaging to satisfy pgadmin4 2.0 dependencies
