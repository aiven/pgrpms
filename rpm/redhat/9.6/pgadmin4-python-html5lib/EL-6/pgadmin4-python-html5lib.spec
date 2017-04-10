%global modulename html5lib

Name:		python-%{modulename}
Summary:	A python based HTML parser/tokenizer
Version:	0.999
Release:	5%{?dist}
Epoch:		1
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{modulename}

Source0:	https://pypi.python.org/packages/source/h/%{modulename}/%{modulename}-%{version}.tar.gz

BuildArch:	noarch
Requires:	python-six
BuildRequires:	python-setuptools
BuildRequires:	python2-devel
BuildRequires:	python-nose
BuildRequires:	python-six

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5
specification for maximum compatibility with major desktop web browsers.

%prep
%setup -q -n %{modulename}-%{version}

%build
%{__python} setup.py build

%install

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc CHANGES.rst README.rst LICENSE
%{python_sitelib}/%{modulename}-*.egg-info
%{python_sitelib}/%{modulename}

%changelog
* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.999-5
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
