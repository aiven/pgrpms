%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname psycopg2

%if 0%{?fedora} > 23
%global with_python3 1
%else
%global with_python3 0
%endif

%if 0%{?with_python3}
 %global	python_runtimes	python python-debug python3 python3-debug
%else
  %if 0%{?rhel} && 0%{?rhel} <= 6
    %global	python_runtimes	python
   %else
    %global python_runtimes python python-debug
  %endif
%endif

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?with_python3}
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%endif # with_python3

Summary:	A PostgreSQL database adapter for Python
Name:		python-%{sname}
Version:	2.6.2
Release:	3%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Group:		Applications/Databases
Url:		http://www.psycopg.org/psycopg/
Source0:	http://www.psycopg.org/psycopg/tarballs/PSYCOPG-2-6/%{sname}-%{version}.tar.gz
Patch0:		setup.cfg.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-debug
%endif # with_python3

%if 0%{?fedora} >= 23 || 0%{?rhel} >= 7
BuildRequires:	python-debug
%endif # Python 2.7

Requires:	postgresql%{pgmajorversion}-libs

Conflicts:	python-%{sname}-zope < %{version}

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%package debug
Summary:	A PostgreSQL database adapter for Python 2 (debug build)
# Require the base package, as we're sharing .py/.pyc files:
Requires:	%{name} = %{version}-%{release}
Group:		Applications/Databases

%description debug
This is a build of the psycopg PostgreSQL database adapter for the debug
build of Python 2.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:	A PostgreSQL database adapter for Python 3

%description  -n python3-%{sname}
This is a build of the psycopg PostgreSQL database adapter for Python 3.

%package -n python3-%{sname}-debug
Summary:	A PostgreSQL database adapter for Python 3 (debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{sname} = %{version}-%{release}

%description -n python3-%{sname}-debug
This is a build of the psycopg PostgreSQL database adapter for the debug
build of Python 3.
%endif # with_python3

%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
for python in %{python_runtimes} ; do
  $python setup.py build
done

# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo

%install

DoInstall() {
  PythonBinary=$1

  Python_SiteArch=$($PythonBinary -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

  %{__mkdir} -p %{buildroot}$Python_SiteArch/%{sname}
  $PythonBinary setup.py install --no-compile --root %{buildroot}

  # We're not currently interested in packaging the test suite.
  %{__rm} -rf %{buildroot}$Python_SiteArch/%{sname}/tests
}

%{__rm} -rf %{buildroot}
for python in %{python_runtimes} ; do
  DoInstall $python
done

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python_sitearch}/%{sname}
%{python_sitearch}/%{sname}/*.py
%{python_sitearch}/%{sname}/*.pyc
%{python_sitearch}/%{sname}/_psycopg.so
%{python_sitearch}/%{sname}/*.pyo
%{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info

%if 0%{?fedora} >= 23 || 0%{?rhel} >= 7
%files debug
%defattr(-,root,root)
%doc LICENSE
%{python_sitearch}/%{sname}/_psycopg_d.so
%endif

%if 0%{?with_python3}
%files -n python3-%{sname}
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python3_sitearch}/%{sname}
%{python3_sitearch}/%{sname}/*.py
%dir %{python3_sitearch}/%{sname}/__pycache__
%{python3_sitearch}/%{sname}/__pycache__/*.pyc
%{python3_sitearch}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitearch}/%{sname}/_psycopg.cpython-3?m*.so

%files -n python3-%{sname}-debug
%defattr(-,root,root)
%doc LICENSE
%{python3_sitearch}/%{sname}/_psycopg.cpython-3*dm*.so
%endif # with_python3

%files doc
%defattr(-,root,root)
%doc doc examples/

%changelog
* Fri Oct 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-3
- Move one .so file into python3-psycopg2 subpackage, per report
  from Oskari Saarenmaa.
- Fix RHEL 6 builds, with custom conditionals.
- Add BR for Python 2.7 environments.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-2
- Move python-debug (PY2 version) package into non-py3 builds.
  We need this at least for pgadmin4.

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2, per changes described at:
  http://www.psycopg.org/psycopg/articles/2016/07/07/psycopg-262-released/

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1
- Create unified spec file for all distros.
- Remove Zope subpackage.
- Minor spec file cleanups

* Mon Feb 9 2015 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6, per changes described at:
  http://www.psycopg.org/psycopg/articles/2015/02/09/psycopg-26-and-255-released/
- Trim changelog
- Merge some changes from Fedora spec file.
