%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:		python-markupsafe
Version:	0.23
Release:	11%{?dist}
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python

Group:		Development/Languages
License:	BSD
URL:		http://pypi.python.org/pypi/MarkupSafe
Source0:	http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel python-setuptools

%description
A library for safe markup escaping.

%prep
%setup -q -n MarkupSafe-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# C code errantly gets installed
%{__rm} %{buildroot}/%{python_sitearch}/markupsafe/*.c

%clean
%{__rm} -rf %{buildroot}

%files
%doc AUTHORS LICENSE README.rst
%{python_sitearch}/*

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.23-11
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.


