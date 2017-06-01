%global debug_package %{nil}

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Command line tool designed to interact with the PostgreSQL Extension Network
Name:		pgxnclient
Version:	1.2.1
Release:	2%{?dist}
Source0:	http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License:	BSD
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://pgxnclient.projects.postgresql.org/
BuildRequires:	python-devel python-setuptools

%description
The PGXN Client is a command line tool designed to interact with the
PostgreSQL Extension Network allowing searching, compiling, installing and
removing extensions in a PostgreSQL installation or database.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{python_sitearch}/%{name}
mkdir -p %{buildroot}%{python_sitearch}/%{name}/tests
%{__python} setup.py install --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%dir %{python_sitearch}/
%dir %{python_sitearch}/%{name}
%dir %{python_sitearch}/%{name}/tests
%{_bindir}/pgxn
%{_bindir}/%{name}
%{python_sitelib}/%{name}/*.py
%{python_sitelib}/%{name}/*.pyc
%{python_sitelib}/%{name}/*.pyo
%{python_sitelib}/%{name}/commands/*.py
%{python_sitelib}/%{name}/commands/*.pyc
%{python_sitelib}/%{name}/commands/*.pyo
%{python_sitelib}/%{name}/libexec/*
%{python_sitelib}/%{name}/tests/*.py
%{python_sitelib}/%{name}/tests/*.pyc
%{python_sitelib}/%{name}/tests/*.pyo
%{python_sitelib}/%{name}/utils/*.py
%{python_sitelib}/%{name}/utils/*.pyc
%{python_sitelib}/%{name}/utils/*.pyo
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/*

%changelog
* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.1-2
- Cosmetic improvements to simplify spec file.

* Thu Sep 26 2013 Jeff Frost <jeff@pgexperts.com> 1.2.1-1
- Update to 1.2.1

* Sat Sep 29 2012 Devrim GUNDUZ <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Jul 27 2012 Devrim GUNDUZ <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Mon Nov 28 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
