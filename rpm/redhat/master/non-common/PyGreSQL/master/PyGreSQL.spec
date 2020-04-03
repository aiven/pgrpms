%if 0%{?fedora} > 26
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
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{srcname}
Version:	5.1
Release:	1%{?dist}.1
Summary:	%{sum}

URL:		http://www.pygresql.org/
# Author states his intention is to dual license under PostgreSQL or Python
# licenses --- this is not too clear from the current tarball documentation,
# but hopefully will be clearer in future releases.
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License:	PostgreSQL or Python

Source0:	http://www.pygresql.org/files/PyGreSQL-%{version}.tar.gz
Patch0:		PyGreSQL-pg%{pgmajorversion}-setup.py-rpm.patch

Provides:	python2-%{name} = %{version}-%{release}
Provides:	python2-%{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:	postgresql%{pgmajorversion}-devel python2-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
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
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
	PATH=%{atpath}/bin/:%{atpath}/sbin:$PATH ; export PATH
%endif
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
%if 0%{?suse_version} >= 1315
%{python2_sitelib}/*.py
%{python2_sitelib}/*.pyc
%else
%{python2_sitelib}/*.py
%{python2_sitelib}/*.pyc
%{python2_sitelib}/*.pyo
%endif
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
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 5.1-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 5.1-1
- Update to 5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-2.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 28 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-2
- Attemp to fix SLES builds.

* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-1
- Update to 5.0.6
- Spec file cleanup, that refers to very old releases.

* Wed Jan 25 2017 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-1
- Initial build for PostgreSQL YUM repository, based on Fedora spec.
