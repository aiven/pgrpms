%global debug_package %{nil}

%if 0%{?fedora} > 27 || 0%{?rhel} >= 7
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

Summary:	Command line tool designed to interact with the PostgreSQL Extension Network
Name:		pgxnclient
Version:	1.3.2
Release:	1%{?dist}
Source0:	https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License:	BSD
Url:		https://github.com/pgxn/pgxnclient
BuildRequires:	python3-devel python3-setuptools

%description
The PGXN Client is a command line tool designed to interact with the
PostgreSQL Extension Network allowing searching, compiling, installing and
removing extensions in a PostgreSQL installation or database.

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root %{buildroot}

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
%dir %{python_sitelib}/
%dir %{python_sitelib}/%{name}
%{_bindir}/pgxn
%{_bindir}/%{name}
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/utils/*.py*
%{python_sitelib}/%{name}/commands/*.py*
%{python_sitelib}/%{name}/libexec/*
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/*
%if 0%{with_python3}
%{python_sitelib}/%{name}/__pycache__/*.p*
%{python_sitelib}/%{name}/commands/__pycache__/*.p*
%{python_sitelib}/%{name}/utils/__pycache__/*.p*
%endif

%changelog
* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Oct 7 2019 Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.1-2
- Cosmetic improvements to simplify spec file.

* Thu Sep 26 2013 Jeff Frost <jeff@pgexperts.com> 1.2.1-1
- Update to 1.2.1

* Sat Sep 29 2012 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Jul 27 2012 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Mon Nov 28 2011 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
