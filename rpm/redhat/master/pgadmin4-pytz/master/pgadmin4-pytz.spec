%if 0%{?fedora} > 24
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global sname pytz

Name:		pgadmin4-%{sname}
Version:	2016.6.1
Release:	3%{?dist}
Summary:	World Timezone Definitions for Python

Group:		Development/Languages
License:	MIT
URL:		http://pytz.sourceforge.net/
Source0:	https://pypi.io/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
# Patch to use the system supplied zoneinfo files
Patch0:		%{name}-zoneinfo.patch

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	pytest
Requires:	tzdata
Provides:	python2-%{sname} = %{version}-%{release}

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
%{__ospython2} setup.py build

%install
%{__ospython2} setup.py install --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python2_sitelib}/%{sname}/*.py
%{__rm} -r %{buildroot}%{python2_sitelib}/%{sname}/zoneinfo

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.txt README.txt CHANGES.txt
%else
%license LICENSE.txt
%doc CHANGES.txt README.txt
%endif
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-3
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
