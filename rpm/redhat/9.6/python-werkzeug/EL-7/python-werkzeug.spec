%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname Werkzeug

Name:		python-werkzeug
Version:	0.11.11
Release:	1%{?dist}
Summary:	The Swiss Army knife of Python web development

Group:		Development/Libraries
License:	BSD
URL:		http://werkzeug.pocoo.org/
Source0:	https://github.com/pallets/werkzeug/archive/%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-sphinx

%description
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n werkzeug-%{version}
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i '1d' tests/multipart/test_collect.py

%build
%{__python} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc docs/_build/html examples

%changelog
* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-1
- Update to 0.11.11
- Use github version, so we don't need the themes tarball anymore.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11.10-4
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
