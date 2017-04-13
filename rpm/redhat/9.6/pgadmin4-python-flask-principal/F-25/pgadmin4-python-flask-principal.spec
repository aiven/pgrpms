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

%global	pypi_name Flask-Principal
%global sname	flask-principal
%global	sum Identity management for Flask applications

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.4.0
Release:	13%{?dist}
Summary:	%{sum}

Group:		Development/Languages
License:	MIT
URL:		https://pypi.python.org/pypi/%{pypi_name}
Source0:	https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# patch adding LICENSE to release tarball accepted upstream, will be included in the next version
Source1:	LICENSE

BuildArch:	noarch

%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%else
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
%endif

%description
Flask-Principal provides a very loose framework to tie in authentication
and user information providers, often located in different parts of a web
application.

%if 0%{?with_python3}
Requires:	python3-flask
Requires:	python3-blinker
%{?python_provide:%python_provide python3-flask-principal}
%else
Requires:	python-flask
Requires:	python-blinker
%{?python_provide:%python_provide python2-flask-principal}
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info
%{__cp} %{SOURCE1} .

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_principal* %{buildroot}%{python3_sitelib}/__pycache__/flask_principal* %{buildroot}%{python3_sitelib}/Flask_Principal-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
popd
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/flask_principal* %{buildroot}%{python2_sitelib}/Flask_Principal-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%doc LICENSE README.rst
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Flask_Principal*.egg-info
%{pgadmin4py3instdir}/flask_principal*
%{pgadmin4py3instdir}/__pycache__/flask_principal*
%else
%{pgadmin4py2instdir}/Flask_Principal*.egg-info
%{pgadmin4py2instdir}/flask_principal*
%endif

%changelog
* Sat Nov 12 2016 evrim Gündüz <devrim@gunduz.org> 0.4.0-13
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
