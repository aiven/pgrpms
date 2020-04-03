%global pypi_name Flask-Gravatar
%global sname flask-gravatar

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Summary:	Small extension for Flask to make usage of Gravatar service easy
Version:	0.5.0
Release:	2%{?dist}
License:	Python
URL:		https://github.com/zzzsochi/%{pypi_name}
Source0:	https://github.com/zzzsochi/%{pypi_name}/archive/v%{version}.tar.gz
%if 0%{?rhel} == 7
Patch0:		%{name}-py36.patch
%endif
BuildArch:	noarch

Requires:	pgadmin4-python3-flask
BuildRequires:	python3-devel python3-setuptools

%description
This is small and simple integration gravatar into flask.

%prep
%setup -q -n %{pypi_name}-%{version}
%if 0%{?rhel} == 7
%patch0 -p0
%endif

%build
# Devrim: Removed this file to surpress build errors.
# Potentially a FIXME for later.
%{__rm} MANIFEST.in
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/flask_gravatar %{buildroot}%{python3_sitelib}/Flask_Gravatar-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%license LICENSE
%doc CHANGES.rst README.rst
%{pgadmin4py3instdir}/Flask_Gravatar*.egg-info
%{pgadmin4py3instdir}/flask_gravatar/*

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-2
- Build with PY3 on RHEL 7.
- Add a patch to fix builds on RHEL 7.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Update to 0.5.0
- Update URLs

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
