%global srcname Werkzeug
%global sname werkzeug

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		pgadmin4-python3-%{sname}
Version:	0.15.4
Release:	2%{?dist}
Summary:	The Swiss Army knife of Python web development

License:	BSD
URL:		http://werkzeug.pocoo.org/
Source0:	https://github.com/pallets/werkzeug/archive/%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

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

%prep
%setup -q -n werkzeug-%{version}
%{__sed} -i 's/\r//' LICENSE.rst
%{__sed} -i '1d' tests/multipart/test_collect.py

%build
%{__ospython} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{srcname}-%{version}*-py%{pyver}.egg-info  %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%license LICENSE.rst
%{pgadmin4py3instdir}/*%{srcname}*.egg-info*
%{pgadmin4py3instdir}/%{sname}

%changelog
* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.15.4-2
- Switch to Python3 on RHEL 7

* Tue Jun 4 2019 Devrim Gündüz <devrim@gunduz.org> - 0.15.4-1
- Update to 0.15.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-4.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Tue Apr 11 2017 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-3
- Move the components under pgadmin web directory, per #2332.

* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-2
- Remove -docs subpackage, sphinx throws out errors on RHEL*.

- Update to 0.11.11
* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11.11-1
- Update to 0.11.11
- Use github version, so we don't need the themes tarball anymore.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.11.10-4
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
