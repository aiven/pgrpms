%global sname   mako

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	1.1.1
Release:	1%{?dist}
BuildArch:	noarch

# Mostly MIT, but _ast_util.py is Python licensed.
# The documentation contains javascript for search licensed BSD or GPLv2
License:	(MIT and Python) and (BSD or GPLv2)
Summary:	Mako template library for Python
URL:		http://www.makotemplates.org/
Source0:	https://github.com/sqlalchemy/mako/archive/rel_%(echo %{version} | sed "s/\./_/g").tar.gz


BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	pgadmin4-python3-markupsafe

%description
Mako is a template library written in Python. It provides a familiar, non-XML\
syntax which compiles into Python modules for maximum performance. Mako's\
syntax and API borrows from the best ideas of many others, including Django\
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded\
Python (i.e. Python Server Page) language, which refines the familiar ideas of\
componentized layout and inheritance to produce one of the most straightforward\
and flexible models available, while also maintaining close ties to Python\
calling and scoping semantics.

This package contains the mako module built for use with python3.

%prep
%setup -q -n mako-rel_%(echo %{version} | sed "s/\./_/g")

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/mako %{buildroot}%{python3_sitelib}/Mako*egg-info %{buildroot}/%{pgadmin4py3instdir}

# These are supporting files for building the docs.  No need to ship
%{__rm} -rf doc/build
%{__rm} -f %{buildroot}%{_bindir}/mako-render

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%doc README.rst
%{pgadmin4py3instdir}/Mako*.egg-info
%{pgadmin4py3instdir}/mako

%changelog
* Mon Feb 10 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-1
- Update to 1.1.1 (#1787962) (#1793184)
