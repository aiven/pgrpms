
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

Name:		pgadmin4-babel
Version:	2.3.4
Release:	2%{?dist}
Summary:	Tools for internationalizing Python applications

Group:		Development/Languages
License:	BSD
URL:		http://babel.pocoo.org/
Source0:	https://files.pythonhosted.org/packages/source/B/Babel/Babel-%{version}.tar.gz
Patch0:		%{name}-remove-pytz-version.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools python3-pytz
BuildRequires:	make python3-sphinx
Requires:	python3-babel python-setuptools
%endif

%if 0%{?rhel} == 6
BuildRequires:	python34-devel python34-setuptools pgadmin4-pytz
BuildRequires:	make python-sphinx10
Requires:	python-babel python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools pytz
BuildRequires:	make python-sphinx
Requires:	python-babel python-setuptools
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-pytz
%endif
%endif

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if 0%{?with_python3}
%package -n pgadmin4-python3-babel
%else
%package -n pgadmin4-python-babel
%endif
Summary:	Library for internationalizing Python applications
Group:		Development/Languages

%if 0%{?fedora} > 25
Requires:	python3-setuptools pytz
%endif

%if 0%{?rhel} == 6
Requires:	pgadmin4-python3-setuptools pgadmin4-pytz
%endif

%if 0%{?rhel} == 7
Requires:	python-setuptools pytz
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	python-pytz
%endif
%endif

%if 0%{?with_python3}
%description -n pgadmin4-python3-babel
%else
%description -n pgadmin4-python-babel
%endif
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%package doc
Summary:	Documentation for Babel
Group:		Development/Languages
Provides:	python-babel-doc = %{version}-%{release}

%description doc
Documentation for Babel

%prep
%setup0 -q -n Babel-%{version}
%patch0 -p1

chmod a-x babel/messages/frontend.py

%build
%{__ospython} setup.py build

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
%{__ospython} setup.py install --skip-build --no-compile --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/babel %{buildroot}%{python3_sitelib}/Babel-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/babel %{buildroot}%{python2_sitelib}/Babel-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

# Remove binary, we don't need it.
%{__rm} %{buildroot}%{_bindir}/pybabel

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE

%if 0%{?with_python3}
%files -n pgadmin4-python3-babel
%else
%files -n pgadmin4-python-babel
%endif
%defattr(-,root,root,-)
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Babel-%{version}-py*.egg-info
%{pgadmin4py3instdir}/babel
%else
%{pgadmin4py2instdir}/Babel-%{version}-py*.egg-info
%{pgadmin4py2instdir}/babel
%endif

%files doc
%doc docs/*

%changelog
* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.4-2
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> - 2.3.4-1
- Update to 2.3.4
  pgadmin4 dependency. Took spec file from Fedora 23 repo.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency. Took spec file from Fedora 23 repo.
