%global __ospython2 %{_bindir}/python2
%global python2_sitearch %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global	srcname	pyrsistent

Summary:	Persistent/Functional/Immutable data structures
Name:		python-%{srcname}
Version:	0.11.13
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
URL:		http://github.com/tobgu/pyrsistent/
BuildRequires:	python-devel
Requires:	python-six
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyrsistent is a number of persistent collections (by some referred to
as functional data structures). Persistent in the sense that they are
immutable.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Persistent/Functional/Immutable data structures
%{?python_provide:%python_provide python3-%{mod_name}}
%{?python_provide:%python_provide python3-flask-sqlalchemy}
BuildRequires:  python3-devel
BuildRequires:  python3-six

%description -n python3-%{srcname}
Pyrsistent is a number of persistent collections (by some referred to
as functional data structures). Persistent in the sense that they are
immutable.

Python 3 version.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}

# Remove bundled egg-info
%{__rm} -r %{srcname}.egg-info

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif # with_python3
%{__ospython2} setup.py build

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
%endif # with_python3
%{__ospython2} setup.py install --skip-build --root %{buildroot}


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%doc README.rst
%{python2_sitearch}/_%{srcname}_*
%{python2_sitearch}/pvectorc.so
%dir %{python2_sitearch}/%{srcname}/
%{python2_sitearch}/%{srcname}/*.py*
%{python2_sitearch}/%{srcname}-%{version}-py%{py2ver}.egg-info/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst
%{python3_sitearch}/__pycache__/_%{srcname}_*.pyc
%{python3_sitearch}/_%{srcname}_version.py
%dir %{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}/*.py*
%{python3_sitearch}/%{srcname}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitearch}/pvectorc.cpython*.so
%{python3_sitearch}/%{srcname}/__pycache__/*.py*

%endif # with_python3

%changelog
* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-2
- Fix packaging errors, that would own /usr/lib64 or so.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.


