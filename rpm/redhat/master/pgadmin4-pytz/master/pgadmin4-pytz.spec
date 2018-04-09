%global sname pytz

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-%{sname}
%else
Name:		pgadmin4-%{sname}
%endif
Version:	2016.6.1
Release:	4%{?dist}
Summary:	World Timezone Definitions for Python

Group:		Development/Languages
License:	MIT
URL:		http://pytz.sourceforge.net/
Source0:	https://pypi.io/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
# Patch to use the system supplied zoneinfo files
Patch0:		%{name}-zoneinfo.patch
BuildArch:	noarch
Requires:	tzdata

%if 0%{?fedora} > 25
BuildRequires: 	python3-devel python3-pytest
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname}
BuildRequires:  python34-devel python34-pytest
%endif

%if 0%{?rhel} == 7
BuildRequires:  python-devel pytest
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytest
%endif
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
%patch0 -p1 -b .zoneinfo

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
chmod +x %{buildroot}%{python3_sitelib}/%{sname}/*.py
%{__rm} -r %{buildroot}%{python3_sitelib}/%{sname}/zoneinfo
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
chmod +x %{buildroot}%{python2_sitelib}/%{sname}/*.py
%{__rm} -r %{buildroot}%{python2_sitelib}/%{sname}/zoneinfo
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.txt README.txt CHANGES.txt
%else
%license LICENSE.txt
%doc CHANGES.txt README.txt
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-3
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
