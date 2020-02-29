%global	pypi_name Flask-Principal
%global sname	flask-principal
%global	sum Identity management for Flask applications

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.4.0
Release:	15%{?dist}
Summary:	%{sum}

License:	MIT
URL:		https://pypi.python.org/pypi/%{pypi_name}
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# patch adding LICENSE to release tarball accepted upstream, will be included in the next version
Source1:	LICENSE

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} >= 30 || 0%{?rhel} == 8
Requires:	python3-flask python3-blinker
%endif

%if 0%{?rhel} == 7
Requires:	pgadmin4-python3-flask pgadmin4-python3-blinker
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif

%description
Flask-Principal provides a very loose framework to tie in authentication
and user information providers, often located in different parts of a web
application.

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info
%{__cp} %{SOURCE1} .

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_principal* %{buildroot}%{python3_sitelib}/__pycache__/flask_principal* %{buildroot}%{python3_sitelib}/Flask_Principal-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README.rst
%else
%license LICENSE
%doc README.rst
%endif
%{pgadmin4py3instdir}/Flask_Principal*.egg-info
%{pgadmin4py3instdir}/flask_principal*
%{pgadmin4py3instdir}/__pycache__/flask_principal*

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-15
- Use Python3 on RHEL 7 as well

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-14.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-14
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 evrim Gündüz <devrim@gunduz.org> 0.4.0-13
- Move the components under pgadmin web directory, per #2332.
- Don't install PY2 version on Fedora systems, because we can
  avoid the need by using Sphinx 3 on them.

* Sat Nov 12 2016 evrim Gündüz <devrim@gunduz.org> 0.4.0-12
- Install both PY2 and PY3 versions for Fedora 24+. Needed to
  build pgadmin3 docs.

* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> 0.4.0-11
- Update spec for pgadmin4 dependency

* Tue Jul 26 2016 Athos Coimbra Ribeiro <ribeiro@fedoraproject.org> - 0.4.0-10
- Add python 2 and 3 subpackages

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013  Richard Marko <rmarko@fedoraproject.org> - 0.4.0-5
- Added missing LICENSE file

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 07 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-3
- Removed upstream egg

* Thu Jul 04 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-2
- Added python-setuptools to BuildRequires
- Added python-blinker to Requires
- Fixed Summary

* Tue Jul 02 2013 Richard Marko <rmarko@fedoraproject.org> - 0.4.0-1
- Initial packaging attempt
