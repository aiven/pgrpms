%global sname	markupsafe
%global mod_name MarkupSafe

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
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
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	0.23
Release:	13%{?dist}.1
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python

License:	BSD
URL:		https://pypi.python.org/pypi/%{mod_name}
Source0:	https://pypi.python.org/packages/source/M/%{mod_name}/%{mod_name}-%{version}.tar.gz

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%description
A library for safe markup escaping.

%prep
%setup -q -n %{mod_name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
# C code errantly gets installed
%{__rm} %{buildroot}/%{python3_sitearch}/%{sname}/*.c
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}%{python3_sitearch}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
# C code errantly gets installed
%{__rm} %{buildroot}/%{python2_sitearch}/%{sname}/*.c
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname} %{buildroot}%{python2_sitearch}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc AUTHORS LICENSE README.rst
%else
%license LICENSE
%doc AUTHORS README.rst
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{mod_name}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{mod_name}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.23-13.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 0:23-13
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 0.23-12
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.23-11
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
