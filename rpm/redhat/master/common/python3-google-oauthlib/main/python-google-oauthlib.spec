#%{?python_enable_dependency_generator}

%global library google-oauthlib

Name:		python3-%{library}
Version:	0.4.1
Release:	1%{?dist}
Epoch:		1
Summary:	oauthlib integration for Google Auth
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python-oauthlib

Source0:	https://github.com/googleapis/google-auth-library-python-oauthlib/archive/v%{version}.tar.gz

BuildArch:	noarch

%description
oauthlib integration for Google Auth

BuildRequires:	python3-devel
BuildRequires:	python3-setuptools

Requires:	python3

%prep
%autosetup -n google-auth-library-python-oauthlib-%{version}

%build
%py3_build

%install
%py3_install

%check

%files
%license LICENSE
%doc README.rst
%{_bindir}/google-oauthlib-tool
%{python3_sitelib}/google_auth_oauthlib-%{version}-py*.egg-info/*
%{python3_sitelib}/google_auth_oauthlib/*.py
%{python3_sitelib}/google_auth_oauthlib/__pycache__/*.py*
%{python3_sitelib}/google_auth_oauthlib/tool/__pycache__/*.py*
%{python3_sitelib}/google_auth_oauthlib/tool/*.py*

%changelog
* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
