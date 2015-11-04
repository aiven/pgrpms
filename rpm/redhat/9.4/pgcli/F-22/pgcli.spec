%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?with_python3}
%global	python_runtimes	python python-debug python3 python3-debug
%else
%global python_runtimes	python
%endif # with_python3

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?with_python3}
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%endif # with_python3

Summary:	A PostgreSQL client that does auto-completion and syntax highlighting
Name:		pgcli
Version:	0.16.3
Release:	1%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Group:		Applications/Databases
Url:		https://github.com/amjith/%{name}
Source0:	https://github.com/amjith/%{name}/archive/v%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-debug
%endif # with_python3

Requires:	python-click => 3.2, python-pygments => 2.0
Requires:	python-sqlparse >= 0.1.14, pyython-%{name} >= 2.5.4
Requires:	python-jedi => 0.8.1

%description
This is a PostgreSQL client that does auto-completion and syntax highlighting.


%if 0%{?fedora} && 0%{?rhel} >= 7
%package debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting (debug build)
# Require the base package, as we're sharing .py/.pyc files:
Requires:	%{name} = %{version}-%{release}
Group:		Applications/Databases

%description debug
This is a build of the for the debug build of Python 2.
%endif

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3

%description  -n python3-%{name}
This is a build of the for the debug build of Python 3.

%if 0%{?fedora} && 0%{?rhel} >= 7
%package -n python3-%{name}-debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3 (debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{name} = %{version}-%{release}

%description -n python3-%{name}-debug
This is a build of the psycopg PostgreSQL database adapter for the debug
build of Python 3.
%endif
%endif # with_python3

%prep
%setup -q

%build
for python in %{python_runtimes} ; do
  $python setup.py build
done

%install

DoInstall() {
  PythonBinary=$1

  Python_SiteArch=$($PythonBinary -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

  mkdir -p %{buildroot}$Python_SiteArch/%{name}
  $PythonBinary setup.py install --no-compile --root %{buildroot}

}

rm -rf %{buildroot}
for python in %{python_runtimes} ; do
  DoInstall $python
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt DEVELOP.rst TODO
%dir %{python_sitearch}/%{name}
#%{python_sitearch}/%{name}/*.py
#%{python_sitearch}/%{name}/*.pyc
#%{python_sitearch}/%{name}/*.pyo
#%{python_sitearch}/%{name}-%{version}-py%{pyver}.egg-info

%if 0%{?fedora} && 0%{?rhel} >= 7
%files debug
%defattr(-,root,root)
%doc LICENSE.txt
%{python_sitearch}/%{name}/_psycopg_d.so
%endif

%if 0%{?with_python3}
%files -n python3-%{name}
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt DEVELOP.rst TODO
%dir %{python3_sitearch}/%{name}
#%{python3_sitearch}/%{name}/*.py
#%{python3_sitearch}/%{name}/_psycopg.cpython-3?m*.so
#%dir %{python3_sitearch}/%{name}/__pycache__
#%{python3_sitearch}/%{name}/__pycache__/*.pyc
#%{python3_sitearch}/%{name}/__pycache__/*.pyo
#%{python3_sitearch}/%{name}-%{version}-py%{py3ver}.egg-info

%if 0%{?fedora} && 0%{?rhel} >= 7
%files -n python3-%{name}-debug
%defattr(-,root,root)
%doc LICENSE
#%{python3_sitearch}/%{name}/_psycopg.cpython-3?dm*.so
%endif
%endif # with_python3

%changelog
* Fri Apr 17 2015 Devrim Gündüz <devrim@gunduz.org> 0.16.3-1
- Initial packaging for PostgreSQL YUM repository.
