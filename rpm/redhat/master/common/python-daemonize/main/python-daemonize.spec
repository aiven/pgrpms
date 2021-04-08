%global modname daemonize

Name:           python3-%{modname}
Version:        2.5.0
Release:        8%{?dist}
Summary:        Library for writing system daemons in Python

License:        MIT
URL:            https://github.com/thesharp/daemonize
Source0:        %{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
daemonize is a library for writing system daemons in Python.

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{modname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}.py
%{python3_sitelib}/__pycache__/%{modname}.*

%changelog
* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-8
- Initial packaging to satisfy pg_chameleon dependency on
  RHEL 7 and 8.
