
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Name:		PyGreSQL
Version:	5.2.1
Release:	1%{?dist}
Summary:	A Python client library for PostgreSQL

URL:		http://www.PyGreSQL.org/
# Author states his intention is to dual license under PostgreSQL or Python
# licenses --- this is not too clear from the current tarball documentation,
# but hopefully will be clearer in future releases.
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License:	PostgreSQL or Python

Source0:	https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-pg%{pgmajorversion}-setup.py-rpm.patch

Provides:	python3-%{name} = %{version}-%{release}
Provides:	python3-%{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

BuildRequires:	postgresql%{pgmajorversion}-devel python3-devel pgdg-srpm-macros

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PostgreSQL is an advanced Object-Relational database management system.
The PyGreSQL package provides a module for developers to use when writing
Python code for accessing a PostgreSQL database.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

# PyGreSQL releases have execute bits on all files
find -type f -exec chmod 644 {} +

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__ospython3} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}

%clean

%files
%license docs/copyright.rst
%doc docs/*.rst
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/*.egg-info
%if 0%{?rhel} <= 7
%{python3_sitearch}/__pycache__/*.pyc
%else
%{python3_sitearch}/__pycache__/*.py{c,o}
%endif

%changelog
* Sun Sep 27 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1
- Update to 5.2.1

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2-1
- Update to 5.2
- Use only PY3

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
