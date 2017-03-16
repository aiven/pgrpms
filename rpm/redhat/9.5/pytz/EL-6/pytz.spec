%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		pytz
Version:	2016.6.1
Release:	2%{?dist}
Summary:	World Timezone Definitions for Python

Group:		Development/Languages
License:	MIT
URL:		http://pytz.sourceforge.net/
Source0:	https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# Patch to use the system supplied zoneinfo files
Patch0:		pytz-zoneinfo.patch

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	pytest
Requires:	tzdata
Provides:	python2-pytz = %{version}-%{release}

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.

%prep
%setup -q
%patch0 -p1 -b .zoneinfo

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python2_sitelib}/pytz/*.py
%{__rm} -r %{buildroot}%{python2_sitelib}/pytz/zoneinfo

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.txt README.txt CHANGES.txt
%else
%license LICENSE.txt
%doc CHANGES.txt README.txt
%endif
%{python2_sitelib}/pytz/
%{python2_sitelib}/*.egg-info

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2016.6.1-2
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
