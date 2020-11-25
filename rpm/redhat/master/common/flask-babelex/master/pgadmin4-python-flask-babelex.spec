%global sname flask-babelex
%global mod_name Flask-BabelEx

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.9.4
Release:	1%{?dist}
Summary:	Adds i18n/l10n support to Flask applications
License:	BSD
URL:		https://github.com/mrjoes/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%if 0%{?fedora} >= 30
BuildRequires:	pgadmin4-python3-flask
Requires:	pgadmin4-python3-flask python3-babel
Requires:	python3-jinja2
%endif

%if 0%{?rhel} == 7
BuildRequires:	pgadmin4-python3-flask
Requires:	pgadmin4-python3-flask pgadmin4-python3-babel
Requires:	pgadmin4-python3-speaklater pgadmin4-python3-jinja2
%endif

%if 0%{?rhel} == 8
BuildRequires:	pgadmin4-python3-flask
Requires:	pgadmin4-python3-flask python3-babel
Requires:	python3-jinja2
%endif

%description
Adds i18n/l10n support to Flask applications with the help of the Babel library.

This is fork of official Flask-Babel extension with following features:

1 -  It is possible to use multiple language catalogs in one Flask application;
2 -  Your extension can package localization file(s) and use them if necessary;
3 -  Does not reload localizations for each request.


%prep
%setup -q -n %{mod_name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_babelex  %{buildroot}%{python3_sitelib}/Flask_BabelEx-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%defattr(-, root, root, -)
%license LICENSE
%doc  README
%{pgadmin4py3instdir}/Flask_BabelEx*.egg-info
%{pgadmin4py3instdir}/flask_babelex/*

%changelog
* Wed Nov 25 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.4-1
- Update to 0.9.4

* Wed Mar 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.3-2
- Switch to PY3 on RHEL 7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.3-1.1
- Rebuild against PostgreSQL 11.0

* Wed Apr 11 2018 Devrim Gündüz <devrim@gunduz.org> - 0.9.3-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
