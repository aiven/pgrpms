Name:		python3-snappy
Version:	0.6.1
Release:	3PGDG%{dist}
Summary:	Python library for the snappy compression library
License:	BSD-3-Clause
URL:		https://github.com/andrix/python-snappy
Source:		https://files.pythonhosted.org/packages/source/p/python-snappy/python-snappy-%{version}.tar.gz
BuildRequires:	python3-devel python3-setuptools
BuildRequires:	gcc-c++ pkgconfig snappy-devel

%description
Python library for the snappy compression library from Google.

%prep
%setup -q -n python-snappy-%{version}
sed -i -e '/^#!\//, 1d' src/snappy/snappy.py

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}


%files
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitearch}/*

%changelog
* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-3PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pghoard on SLES 15.
