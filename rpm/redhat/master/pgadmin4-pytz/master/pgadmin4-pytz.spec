%global sname pytz

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-%{sname}
Version:	2018.9
Release:	2%{?dist}
Summary:	World Timezone Definitions for Python

License:	MIT
URL:		http://pytz.sourceforge.net/
Source0:	https://pypi.io/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch
Requires:	tzdata

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
BuildRequires:	python3-devel python3-pytest
%endif

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
chmod +x %{buildroot}%{python3_sitelib}/%{sname}/*.py
%{__rm} -r %{buildroot}%{python3_sitelib}/%{sname}/zoneinfo
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%license LICENSE.txt
%doc README.txt
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 2018.9-2
- Switch to Python3 on RHEL 7.

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2018.9-1
- Update to 2018.09

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2018.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 2018.3-1
- Update to 2018.3
- Disable patches for now.

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-3
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
