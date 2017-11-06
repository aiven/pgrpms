%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%{!?python2_sitearch: %global python2_sitearch %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global sname	markupsafe
%global mod_name MarkupSafe

Name:		pgadmin4-python-markupsafe
Version:	0.23
Release:	12%{?dist}
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python

Group:		Development/Languages
License:	BSD
URL:		https://pypi.python.org/pypi/%{mod_name}
Source0:	https://pypi.python.org/packages/source/M/%{mod_name}/%{mod_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel python-setuptools

%description
A library for safe markup escaping.

%prep
%setup -q -n %{mod_name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__ospython2} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# C code errantly gets installed
%{__rm} %{buildroot}/%{python2_sitearch}/markupsafe/*.c
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname} %{buildroot}%{python2_sitearch}/%{mod_name}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%doc AUTHORS LICENSE README.rst
%{pgadmin4py2instdir}/*%{mod_name}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 0.23-12
- Move the components under pgadmin web directory, per #2332.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 0.23-11
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
