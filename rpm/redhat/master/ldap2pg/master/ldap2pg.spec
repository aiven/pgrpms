%global debug_package %{nil}
%global sname ldap2pg

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if 0%{?with_python3}
 %global        python_runtimes python python-debug python3 python3-debug
%else
  %if 0%{?rhel} && 0%{?rhel} <= 6 || 0%{?suse_version} >= 1315
    %global     python_runtimes python
   %else
    %global python_runtimes python python-debug
  %endif
%endif

Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
Name:		python-%{sname}
Version:	4.6
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz

BuildRequires:	python-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-debug
%endif # with_python3

%if 0%{?fedora} >= 23 || 0%{?rhel} >= 7
BuildRequires:	python-debug
%endif # Python 2.7
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	postgresql%{pgmajorversion}-libs

%description
Swiss-army knife to synchronize Postgres roles and ACLs from any LDAP directory.

Features:

* Creates, alter and drops PostgreSQL roles from LDAP queries.
* Creates static roles from YAML to complete LDAP entries.
* Manage role members (alias groups).
* Grant or revoke custom ACL statically or from LDAP entries.
* Dry run.
* Logs LDAP queries as ldapsearch commands.
* Logs every SQL queries.
* Reads settings from YAML config file.

%package debug
Summary:	Synchronize Postgres roles and ACLs from any LDAP directory (debug build)
# Require the base package, as we're sharing .py/.pyc files:
Requires:	%{name} = %{version}-%{release}
Group:		Applications/Databases

%description debug
This is a build of the ldap2pg for the debug build of Python 2.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description  -n python3-%{sname}
This is a build of the ldap2pg for Python 3.

%package -n python3-%{sname}-debug
Summary:	Synchronize Postgres roles and ACLs from any LDAP directory (Python 3 debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{sname} = %{version}-%{release}

%description -n python3-%{sname}-debug
This is a build of the psycopg PostgreSQL database adapter for the debug
build of Python 3.
%endif # with_python3

%package doc
Summary:	Documentation for ldap2pg
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the ldap2pg package.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
	PATH=%{atpath}/bin/:%{atpath}/sbin:$PATH ; export PATH
%endif
for python in %{python_runtimes} ; do
  $python setup.py build
done

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
%doc README.rst
%{_bindir}/%{sname}
%dir %{python_sitelib}/%{sname}
%{python2_sitelib}/%{sname}/*.py
%{python_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info
%if 0%{?suse_version} >= 1315
%{python_sitelib}/%{sname}/*.py
%else
%{python_sitelib}/%{sname}/*.py
%{python_sitelib}/%{sname}/*.pyc
%{python_sitelib}/%{sname}/*.pyo
%endif

%if 0%{?with_python3}
%files -n python3-%{sname}
%defattr(-,root,root)
%doc README.rst LICENSE
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info

%files -n python3-%{sname}-debug
%defattr(-,root,root)
%dir %{python3_sitelib}/%{sname}/__pycache__
%{python3_sitelib}/%{sname}/__pycache__/*
%endif # with_python3

%files doc
%defattr(-,root,root)
%doc docs/

%changelog
* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> 4.6-1
- Update to 4.6

* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Sat Aug 5 2017 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Initial packaging for PostgreSQL YUM repository.
