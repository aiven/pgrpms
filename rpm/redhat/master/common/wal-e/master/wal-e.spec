%global	debug_package %{nil}

%if 0%{?rhel} && 0%{?rhel} >= 7
# Note to RHEL 7 users: python-gevent exists in extras repo.
# Install WAL-E with the following command:
# yum --enablerepo extras install wal-e
Requires:	python-gevent
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%else
Requires:	python3-gevent => 1.1.1
%endif

BuildRequires:	python3-devel, python3-setuptools
%global __python3	/usr/bin/python3

%{expand: %%global pyver %(echo `%__python3 -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global	python3_sitelib %(%__python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	Continuous Archiving for Postgres
Name:		wal-e
Version:	1.1.1
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/%{name}/%{name}

%description
WAL-E is a program designed to perform continuous archiving of PostgreSQL
WAL files and base backups.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%__python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{python3_sitelib}/wal_e/
%{_bindir}/%{name}
%{python3_sitelib}/wal_e-%{version}-py%{pyver}.egg-info/*

%changelog
* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Sun Feb 19 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2
- Add RHEL 7 support, per request from Martín Marqués.
- Add missing BR

* Mon Nov 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
