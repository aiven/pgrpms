%global sname	markupsafe
%global mod_name MarkupSafe

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	0.23
Release:	14%{?dist}
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python

License:	BSD
URL:		https://pypi.python.org/pypi/%{mod_name}
Source0:	https://pypi.python.org/packages/source/M/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildRequires:	python3-devel python3-setuptools

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
# C code errantly gets installed
%{__rm} %{buildroot}/%{python3_sitearch}/%{sname}/*.c
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}%{python3_sitearch}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%doc AUTHORS README.rst
%{pgadmin4py3instdir}/*%{mod_name}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Wed Mar 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.23-14
- Switch to PY3 on RHEL 7

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
