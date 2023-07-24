%{!?with_python3:%global with_python3 1}

%if 0%{?rhel} == 8
%global __ospython %{_bindir}/python3.9
%else
%global __ospython %{_bindir}/python3
%endif

%if 0%{?fedora} >= 35
%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Summary:	Top like application for PostgreSQL server activity monitoring
Name:		pg_activity
Version:	3.4.2
Release:	1PGDG%{?dist}
License:	GPLv3
Url:		https://github.com/dalibo/%{name}/
Source0:	https://github.com/dalibo/%{name}/archive/v%{version}.tar.gz
BuildArch:	noarch

%if 0%{?rhel} == 8
Requires:	python39 python39-attrs
Requires:	python39-six python39-psutil
Requires:	python39-psycopg2 >= 2.8.6
Requires:	python39-humanize >= 3.13.1
Requires:	python39-blessed
Requires:	python39-wcwidth
%else
Requires:	python3-blessed
Requires:	python3 >= 3.9 python3-attrs
Requires:	python3-six python3-psutil
Requires:	python3-psycopg3 >= 3.1.8
Requires:	python3-humanize >= 2.6.0
Requires:	python3-wcwidth
%endif

BuildRequires:	python3-setuptools >= 0.6.10

%description
top like application for PostgreSQL server activity monitoring.

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}%{_mandir}/man1/

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/*
%{python_sitelib}/pgactivity/*.py*
%{python_sitelib}/pgactivity/__pycache__/*.pyc
%{python_sitelib}/pgactivity/queries/*.py
%{python_sitelib}/pgactivity/queries/*.sql
%{python_sitelib}/pgactivity/queries/__pycache__/*.pyc

%changelog
* Mon Jul 24 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4.2-1PGDG
- Update to 3.4.2
- Add PGDG branding

* Thu Jun 1 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1

* Wed Apr 5 2023 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0
- Adjust RHEL 8 dependencies for Python 3.9

* Mon Mar 6 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Thu Mar 2 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0
- Switch to psycopg3

* Fri Nov 11 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-1
- Update to 3.0.1

* Mon Sep 19 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-2
- Add proper RHEL 8 support.

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0
- Remove support for RHEL 7, as this new version requires
  Python 3.9.

* Thu Apr 28 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1

* Wed Apr 20 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0
- Fix for Python 3.10+ builds

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.5-1
- Update to 2.1.5

* Sun Mar 21 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1
- Update to 2.1.3

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
