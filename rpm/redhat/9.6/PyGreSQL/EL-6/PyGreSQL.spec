%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6

%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%global sum	A Python client library for PostgreSQL
%global srcname	PyGreSQL

Name:		%{srcname}
Version:	5.0.3
Release:	1%{?dist}
Summary:	%{sum}

Group:		Applications/Databases
URL:		http://www.pygresql.org/
# Author states his intention is to dual license under PostgreSQL or Python
# licenses --- this is not too clear from the current tarball documentation,
# but hopefully will be clearer in future releases.
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License:	PostgreSQL or Python

Source0:	http://www.pygresql.org/files/PyGreSQL-%{version}.tar.gz
Patch0:		PyGreSQL-setup.py-rpm.patch

# PyGreSQL was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  Note there is no
# intention of changing the version numbers in future.
Provides:	postgresql-python = 8.5.0-1
Obsoletes:	postgresql-python < 8.5
Provides:	python2-%{name} = %{version}-%{release}
Provides:	python2-%{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:	postgresql%{pgmajorversion}-devel python2-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
%endif

%description
PostgreSQL is an advanced Object-Relational database management system.
The PyGreSQL package provides a module for developers to use when writing
Python code for accessing a PostgreSQL database.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:	%{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%endif

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p0

# PyGreSQL releases have execute bits on all files
find -type f -exec chmod 644 {} +

%build
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%clean

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc docs/copyright.rst docs/*.rst
%else
%license docs/copyright.rst
%doc docs/*.rst
%endif
%{python2_sitelib}/*.so
%{python2_sitelib}/*.py
%{python2_sitelib}/*.pyc
%{python2_sitelib}/*.pyo
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%license docs/copyright.rst
%doc docs/*.rst
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.py{c,o}
%{python3_sitearch}/*.egg-info
%endif

%changelog
* Wed Jan 25 2017 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-1
- Initial build for PostgreSQL YUM repository, based on Fedora spec.
