%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname Werkzeug
%global sname werkzeug

%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

Name:		pgadmin4-python-werkzeug
Version:	0.11.11
Release:	3%{?dist}
Summary:	The Swiss Army knife of Python web development

Group:		Development/Libraries
License:	BSD
URL:		http://werkzeug.pocoo.org/
Source0:	https://github.com/pallets/werkzeug/archive/%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools

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
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i '1d' tests/multipart/test_collect.py

%build
%{__ospython2} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{srcname}-%{version}*-py%{py2ver}.egg-info  %{buildroot}/%{pgadmin4py2instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{pgadmin4py2instdir}/*%{srcname}*.egg-info*
%{pgadmin4py2instdir}/%{sname}

%changelog
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
