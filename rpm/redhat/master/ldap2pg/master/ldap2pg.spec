%global debug_package %{nil}
%global sname ldap2pg

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%if 0%{?fedora} > 26 || 0%{?rhel} >= 8
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
 %global	python_runtimes python2 python3
%else
 %global	python_runtimes python2
%endif

Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
Name:		python-%{sname}
Version:	5.0
Release:	1%{?dist}
License:	BSD
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz

BuildRequires:	python-devel
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

Requires:	postgresql%{pgmajorversion}-libs

%if 0%{?with_python3}
Requires:	python3-psycopg2 python3-ldap python3-yaml python3-setuptools
%else
Requires:	python-psycopg2, python-ldap python-yaml python-setuptools
%endif

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

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description  -n python3-%{sname}
This is a build of the ldap2pg for Python 3.
%endif

%package doc
Summary:	Documentation for ldap2pg
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
%{python_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info
%if 0%{?suse_version} >= 1315
 %{python_sitelib}/%{sname}/*.py
%else
 %{python_sitelib}/%{sname}/*.py*
%endif

%if 0%{?with_python3}
%files -n python3-%{sname}
%defattr(-,root,root)
%doc README.rst LICENSE
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%endif

%files doc
%defattr(-,root,root)
%doc docs/

%changelog
* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 5.0-1
- Update to 5.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 4.18-1
- Update to 4.18

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.12-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 21 2018 Devrim Gündüz <devrim@gunduz.org> 4.12-1
- Update to 4.12

* Sun Jul 1 2018 Devrim Gündüz <devrim@gunduz.org> 4.11-1
- Update to 4.11

* Thu May 24 2018 Devrim Gündüz <devrim@gunduz.org> 4.9-1
- Update to 4.9
- Fix various packaging issues, per Magnus

* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> 4.6-1
- Update to 4.6

* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Sat Aug 5 2017 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Initial packaging for PostgreSQL YUM repository.
