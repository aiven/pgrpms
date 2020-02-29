%global sname	flask-babel
%global mod_name	Flask-Babel

%if 0%{?fedora} > 27 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/


Name:		pgadmin4-python3-%{sname}
Version:	0.11.1
Release:	5%{?dist}
Summary:	Adds i18n/l10n support to Flask applications
License:	BSD
URL:		http://github.com/mitsuhiko/%{sname}/
Source0:	https://github.com/python-babel/flask-babel/archive/v%{version}.tar.gz
BuildArch:	noarch


%if 0%{?fedora} > 27
BuildRequires:	python3-babel python3-devel
BuildRequires:	python3-flask python3-setuptools
BuildRequires:	python3-speaklater python3-pytz
Requires:	python3-babel python3-flask
Requires:	python3-speaklater python3-pytz
%endif

%if 0%{?rhel} >= 7
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	pgadmin4-python3-speaklater
Requires:	python3-babel python3-flask
Requires:	pgadmin4-python3-speaklater
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-babel pgadmin4-python3-flask
BuildRequires:	pgadmin4-pytz
Requires:	pgadmin4-pytz
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-babel python3-flask python3-pytz
Requires:	python3-pytz
%endif

%description
Adds i18n/l10n support to Flask applications with the help of the Babel library.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_babel %{buildroot}%{python3_sitelib}/Flask_Babel-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%doc docs LICENSE
%{pgadmin4py3instdir}/*.egg-info/
%{pgadmin4py3instdir}/flask_babel/*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.11.1-5
- Switch to PY3 on RHEL 7.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.11.1-4.1
- Rebuild against PostgreSQL 11.0

* Thu Apr 5 2018 Devrim Gündüz <devrim@gunduz.org> - 0.11.1-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.11.1-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Sat Sep 10 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.1-2
- Various updates for pgadmin4 packaging.

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
