%global debug_package %{nil}
%global sname pgldapsync

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	A tool for syncing LDAP users to Postgres Roles
Name:		%{sname}
Version:	1.0.0
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/enterprisedb/pgldapsync
Source0:	https://github.com/EnterpriseDB/pgldapsync/archive/refs/tags/pgldapsync-%{version}.tar.gz

BuildRequires:	python3-devel >= 3.5 pgdg-srpm-macros >= 1.0.17

Requires:	libpq5 >= 10.0

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This Python module allows you to synchronise Postgres login roles with users
in an LDAP directory.

pgldapsync requires Python 3.5 or later.

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

# Change /usr/bin/python to /usr/bin/python3 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done

%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info/*
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{sname}/config.ini.example
%{python3_sitelib}/%{sname}/config_default.ini
%{python3_sitelib}/%{sname}/ldaputils/*.py*
%{python3_sitelib}/%{sname}/ldaputils/__pycache__/*.py*
%{python3_sitelib}/%{sname}/pgutils/*.py
%{python3_sitelib}/%{sname}/pgutils/__pycache__/*.py*

%changelog
* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for the PostgreSQL RPM repository.
