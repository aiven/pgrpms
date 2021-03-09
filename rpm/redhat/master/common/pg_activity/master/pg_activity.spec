%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
BuildRequires:	python3-setuptools >= 0.6.10

Summary:	Top like application for PostgreSQL server activity monitoring
Name:		pg_activity
Version:	2.1.0
Release:	1%{?dist}
License:	GPLv3
Url:		https://github.com/dalibo/%{name}/
Source0:	https://github.com/dalibo/%{name}/archive/v%{version}.tar.gz
BuildArch:	noarch
Requires:	python3 >= 3.6, python3-psycopg2 >= 2.8.3
%if 0%{?rhel} == 7
Requires:	python36-psutil python36-humanize
Requires:	python36-blessed python36-attrs
%endif
%if 0%{?fedora} > 27 || 0%{?rhel} == 8
Requires:	python3-psutil python3-humanize
Requires:	python3-blessed python3-attrs
%endif

%description
top like application for PostgreSQL server activity monitoring.

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --with-man -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/
%{_mandir}/man1/%{name}.1.gz
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/*
%{python_sitelib}/pgactivity/*.py*
%{python_sitelib}/pgactivity/__pycache__/*.pyc
%{python_sitelib}/pgactivity/queries/*.py
%{python_sitelib}/pgactivity/queries/*.sql
%{python_sitelib}/pgactivity/queries/__pycache__/*.pyc

%changelog
* Tue Mar 9 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Thu Jan 28 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Jan 25 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Add missing dependencies, per report from Marcin Gozdalik
  and Denis Laxalde.

* Thu Jan 21 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Mon Oct 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1
- Update to 1.6.2

* Thu May 14 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1

* Thu May 7 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1
- Update to 1.6.0

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0, per #3160

* Fri Oct 7 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Mon Oct 3 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Add a patch to fix compatibility with PostgreSQL 9.6. This
  patch will be removed when next version is out.

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Wed Feb 4 2015 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0
- Remove patch0
- Fix rpmlint warnings in spec file.

* Thu Feb 27 2014 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Sat Dec 28 2013 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0
- Fix packaging issues
- Update description and summary

* Thu Dec 20 2012 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-1
- Initial packaging, based on the spec by Marco Neciarini
