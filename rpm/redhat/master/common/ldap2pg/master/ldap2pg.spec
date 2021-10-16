%global debug_package %{nil}
%global sname ldap2pg

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global	python_runtimes python3

Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
Name:		python3-%{sname}
Version:	5.6
Release:	1%{?dist}
License:	BSD
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz

BuildRequires:	python3-devel pgdg-srpm-macros

Obsoletes:	python-ldap2pg < 5.1

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

Requires:	libpq5 >= 10.0

Requires:	python3-psycopg2 python3-ldap python3-setuptools
%if 0%{?rhel} == 7
Requires:	python36-yaml
%else
Requires:	python3-yaml
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

%package doc
Summary:	Documentation for ldap2pg
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the ldap2pg package.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
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
%doc README.rst LICENSE
%{_bindir}/%{sname}
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%if 0%{?suse_version} >= 1315
%else
%{python3_sitelib}/%{sname}/__pycache__/*
%endif

%files doc
%defattr(-,root,root)
%doc docs/

%changelog
* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 5.6-1
- Update to 56

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 5.5-1
- Update to 5.5

* Wed Nov 18 2020 Devrim Gündüz <devrim@gunduz.org> - 5.4-2
- Fix RHEL 7 dependency, per report from Magnus.

* Sun Jun 14 2020 Devrim Gündüz <devrim@gunduz.org> - 5.4-1
- Update to 5.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2-2
- Depend on "libpq5", which is now provided by the latest
  PostgreSQL 10+ minor update set.

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2-1
- Update to 5.2
- Switch to PY3-only
- Depend on versionless postgresql-libs

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
