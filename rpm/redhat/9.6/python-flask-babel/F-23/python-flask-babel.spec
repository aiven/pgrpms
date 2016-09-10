%if 0%{?fedora} > 21
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


%global pkg_name	flask-babel
%global mod_name	Flask-Babel

Name:		python-%{pkg_name}
Version:	0.11.1
Release:	1%{?dist}
Summary:	Adds i18n/l10n support to Flask applications
Group:		Development/Libraries
License:	BSD
URL:		http://github.com/mitsuhiko/%{pkg_name}/
Source0:	https://github.com/python-babel/flask-babel/archive/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python2-babel, python3-babel
BuildRequires:	python2-devel, python3-devel
BuildRequires:	python-flask, python3-flask
BuildRequires:	python-setuptools
BuildRequires:	python2-speaklater, python3-speaklater
BuildRequires:	pytz, python3-pytz
Patch0:		%{name}-tests.patch
Patch1:		%{name}-more-tests.patch
%{?python_provide:%python_provide python-%{pkg_name}}

%description
Adds i18n/l10n support to Flask applications with the help of the Babel library.

%package -n python3-%{pkg_name}
Summary:	Adds i18n/l10n support to Flask applications
Requires:	python3-babel
Requires:	python3-flask
Requires:	python3-speaklater
Requires:	python3-pytz
%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name}
Adds i18n/l10n support to Flask applications with the help of the Babel library.

%prep
%setup -q -n %{pkg_name}-%{version}
%if 0%{?epel} == 7
%patch0 -p1 -R
%endif
%if 0%{?fedora} > 24
%patch1 -p1
%endif

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files
%doc docs LICENSE
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/flask_babel/*.py*

%files -n python3-%{pkg_name}
%doc docs LICENSE
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_babel/*

%changelog
* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.1-1
- Update to 0.11.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.9-6
- Rebuild to properly provide python-flask-babel

* Tue Jun 28 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.9-5
- Add python3 subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 17 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.9-2
- Revert patch to pass check with older Babel (#1175391).

* Fri Jul 18 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.9-1
- Update to latest upstream release (#1106770).

* Thu Jul 17 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-6
- Add patch to work with latest Babel (#1106770).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-4
- Add missing python-setuptools build requires (#839071)
- Remove wrongly installed .gitignore

* Fri Aug 17 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-3
- Add missing build requires for proper chroot build
- Correct spec file to make %%check work without having package installed

* Sun Aug 5 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-2
- No need to set CFLAGS for noarch (#839071)
- Add %%check section (#839071)

* Tue Jul 10 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-1
- Initial python-flask-babel spec.
