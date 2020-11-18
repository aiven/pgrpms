%global sname email-validator

%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

Name:		pgadmin4-python3-%{sname}

Version:	1.1.1
Release:	2%{?dist}
Summary:	A robust email syntax and deliverability validation library

License:	CC0
URL:		https://github.com/JoshData/python-email-validator
Source0:	%{url}/archive/v%{version}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%description
This library validates that address are of the form x@y.com. This is the sort
of validation you would want for a login form on a website.

Key features:

- Good for validating email addresses used for logins/identity.
- Friendly error messages when validation fails (appropriate to show to end
  users).
- (optionally) Checks deliverability: Does the domain name resolve?
- Supports internationalized domain names and (optionally) internationalized
  local parts.
- Normalizes email addresses (important for internationalized addresses!).

BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-dns

%prep
%autosetup -n python-%{sname}-%{version}
%{__rm} -rf %{sname}.egg-info

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_bindir}/email_validator
%{python3_sitelib}/email_validator/
%{python3_sitelib}/email_validator-%{version}-py*.egg-info

%changelog
* Wed Nov 18 2020 Devrim Gündüz <devrim@gunduz.org> -  1.1.1-2
- Initial packaging for PostgreSQL RPM repository to satisfy pgadmin4 dependency.
