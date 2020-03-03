%global sname itsdangerous

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:        0.24
Release:        11%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
License:        BSD
URL:            http://pythonhosted.org/%{sname}/
Source0:        https://pypi.python.org/packages/source/i/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:	python3-devel python3-setuptools

%description
Itsdangerous is a Python library for passing data through untrusted
environments (for example, HTTP cookies) while ensuring the data is not
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the
implementation on the Django signing module. It also however supports JSON Web
Signatures (JWS).

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -r *.egg-info

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}%{python3_sitelib}/%{sname}.py* %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%license LICENSE
%doc CHANGES README
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}.cpython-*.py*
%{pgadmin4py3instdir}/%{sname}.cpython-*.py*
%endif

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.24-11
- Switch to PY3 on RHEL 7, too.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.24-10.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 0.24-10
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 0.24-9
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.24-8
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

