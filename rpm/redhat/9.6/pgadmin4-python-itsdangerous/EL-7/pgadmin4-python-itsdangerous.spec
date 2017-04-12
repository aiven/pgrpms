%global sname itsdangerous
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

Name:           pgadmin4-python-%{sname}
Version:        0.24
Release:        9%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
License:        BSD
URL:            http://pythonhosted.org/itsdangerous/
Source0:        http://pypi.python.org/packages/source/i/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools

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
%{__ospython2} setup.py build

%install
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}.py* %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%doc LICENSE CHANGES README
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}.py*

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 0.24-9
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.24-8
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

