%global debug_package %{nil}
%global	sname ldap2pg

%if 0%{?fedora} >= 35
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global python_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
Name:		python3-%{sname}
Version:	5.9
Release:	2%{?dist}
License:	BSD
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz

BuildRequires:	python3-devel pgdg-srpm-macros

Obsoletes:	python-ldap2pg < 5.1

Requires:	libpq5 >= 10.0

Requires:	python3-psycopg2 python3-ldap python3-setuptools

%if 0%{?rhel} == 7
Requires:	python36-PyYAML
%endif
%if 0%{?suse_version} >= 1315
Requires:	python3-PyYAML
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	python3-pyyaml
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
%{__python3} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{python_sitearch}
%{__python3} setup.py install --no-compile --root %{buildroot}

# Install sample config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__cp} %{sname}.yml %{buildroot}%{_sysconfdir}

# We're not currently interested in packaging the test suite.
%{__rm} -rf %{buildroot}%{python_sitearch}/%{sname}/tests

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.rst LICENSE
%config %{_sysconfdir}/%{sname}.yml
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
* Wed Jun 14 2023 Devrim Gündüz <devrim@gunduz.org> - 5.9-2
- Install sample config file
- Simplify install section, no need to use a function as we
  support only one Python version.

* Wed Apr 12 2023 Devrim Gündüz <devrim@gunduz.org> - 5.9-1
- Update to 5.9

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 5.8-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 5.8-1
- Update to 5.8

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 5.7-1
- Update to 5.7

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 5.6-1
- Update to 5.6

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
