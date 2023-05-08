%global		sname terminaltables
Summary:	Generate tables in terminals from list of strings
Name:		python3-%{sname}
Version:	3.1.10
Release: 	7%{?dist}
License:	MIT
URL:		https://github.com/matthewdeanmartin/terminaltables
Source0:	https://github.com/matthewdeanmartin/terminaltables/archive/v%{version}.tar.gz
Patch0:		python3-terminaltables-reqs.patch
Patch1:		python3-terminaltables-poetry-core.patch
BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	pyproject-rpm-macros
%description
Easily draw tables in terminal/console applications (written in\
Python) from a list of lists of strings. Supports multi-line rows.

%prep
%autosetup -n terminaltables-%{version}

%generate_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{sname}

%check
%tox || :

%files -n python3-terminaltables -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md

%changelog
* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.10-7
- Initial packaging for the PostgreSQL RPM repository to satisfy
  python3-cli-helpers on RHEL 8. Took spec file from EPEL 9
