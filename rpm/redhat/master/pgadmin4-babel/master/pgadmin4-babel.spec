%if 0%{?fedora} > 23
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
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/


Name:           pgadmin4-babel
Version:        1.3
Release:        1%{?dist}
Summary:        Tools for internationalizing Python applications

Group:          Development/Languages
License:        BSD
URL:            http://babel.pocoo.org/
Source0:        https://pypi.python.org/packages/source/B/Babel/Babel-%{version}.tar.gz
Patch0:         %{name}-remove-pytz-version.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytz

# build the documentation
BuildRequires:  make
BuildRequires:  python-sphinx

Requires:       python-babel
Requires:       python-setuptools

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%package -n pgadmin4-python-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

Requires:       python-setuptools
Requires:       pytz

%description -n pgadmin4-python-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%package doc
Summary:        Documentation for Babel
Group:          Development/Languages
Provides:       python-babel-doc = %{version}-%{release}

%description doc
Documentation for Babel

%prep
%setup0 -q -n Babel-%{version}
%patch0 -p1

chmod a-x babel/messages/frontend.py

%build
%{__ospython2} setup.py build

%if 0%{?rhel} && 0%{?rhel} <= 6
:
%else
# build the docs and remove all source files (.rst, Makefile) afterwards
cd docs
make html
%{__mv} _build/html .
%{__rm} -rf _* api *.rst conf.py objects.inv Makefile make.bat
%{__mv} html/* .
%{__rm} -rf html
%endif

%install
%{__rm} -rf %{buildroot}

%{__ospython2} setup.py install --skip-build --no-compile --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/babel %{buildroot}%{python2_sitelib}/Babel-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
# Remove binary, we don't need it.
%{__rm} %{buildroot}%{_bindir}/pybabel
%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README AUTHORS

%files -n pgadmin4-python-babel
%defattr(-,root,root,-)
%{pgadmin4py2instdir}/Babel-%{version}-py*.egg-info
%{pgadmin4py2instdir}/babel

%files doc
%doc docs/*

%changelog
* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency. Took spec file from Fedora 23 repo.
