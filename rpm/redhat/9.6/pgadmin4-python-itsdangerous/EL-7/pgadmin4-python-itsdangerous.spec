%global upstream_name itsdangerous


Name:           python-%{upstream_name}
Version:        0.24
Release:        8%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
License:        BSD
URL:            http://pythonhosted.org/itsdangerous/
Source0:        http://pypi.python.org/packages/source/i/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Itsdangerous is a Python library for passing data through untrusted
environments (for example, HTTP cookies) while ensuring the data is not
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the
implementation on the Django signing module. It also however supports JSON Web
Signatures (JWS).

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python 3 library for passing trusted data to untrusted environments

%description -n python3-%{upstream_name}
Itsdangerous is a Python 3 library for passing data through untrusted
environments (for example, HTTP cookies) while ensuring the data is not
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the
implementation on the Django signing module. It also however supports JSON Web
Signatures (JWS).
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
%{__rm} -r *.egg-info

%if %{with python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc LICENSE CHANGES README
%{python_sitelib}/%{upstream_name}.py*
%{python_sitelib}/%{upstream_name}*.egg-info

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.24-8
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

