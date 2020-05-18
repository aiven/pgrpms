%{?python_enable_dependency_generator}

%global library google-auth

%if 0%{?rhel} == 7
%global py3 python%{python3_pkgversion}
%else
%global py3 python3
%endif

Name:		python-%{library}
Version:	1.14.3
Release:	1%{?dist}
Epoch:		1
Summary:	Google Auth Python Library
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python

Source0:	https://github.com/googleapis/google-auth-library-python/archive/v%{version}.tar.gz

BuildArch:	noarch

%description
Google Auth Python Library

%package -n %{py3}-%{library}
Summary:    Google Auth Python Library
%{?python_provide:%python_provide %{py3}-%{library}}

BuildRequires:	%{py3}-devel
BuildRequires:	%{py3}-setuptools
BuildRequires:	git
%if %{undefined __pythondist_requires}
Requires:	%{py3}-pyasn1
Requires:	%{py3}-pyasn1-modules
Requires:	%{py3}-rsa
Requires:	%{py3}-six
Requires:	%{py3}-cachetools
%endif

%description -n %{py3}-%{library}
Python client for the kubernetes API.

%prep
%autosetup -n google-auth-library-python-%{version}

#Allow newer cachetools
sed -i 's/<3\.2/<5.0/g' setup.py

%build
%py3_build

%install
%py3_install

%check

%files -n %{py3}-%{library}
%license LICENSE
%{python3_sitelib}/google/auth
%{python3_sitelib}/google/oauth2
%{python3_sitelib}/google_auth-%{version}*.egg-info
%{python3_sitelib}/google_auth-%{version}*.pth

%changelog
* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.3-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
