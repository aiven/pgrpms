%global debug_package %{nil}

%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if 0%{?fedora} > 23 || 0%{?rhel} >= 8
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

%if 0%{?with_python3}
%global	python_runtimes	python2 python2-debug python3 python3-debug
%else
%global python_runtimes	python2 python2-debug
%endif

Summary:	A PostgreSQL client that does auto-completion and syntax highlighting
Name:		pgcli
Version:	2.1.1
Release:	1%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/amjith/%{name}
Source0:	https://github.com/amjith/%{name}/archive/v%{version}.tar.gz

BuildRequires:	python2-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-debug
%endif

%if 0%{?with_python3}
Requires:	python3-click => 3.2, python3-pygments => 2.0
Requires:	python3-sqlparse >= 0.1.14, python3-%{name}
Requires:	python3-jedi => 0.8.1 python3-setproctitle >= 1.1.9
Requires:	python3-wcwidth >= 0.1.6 python3-humanize >= 0.5.1
Requires:	python3-configobj >= 5.0.6 python3-prompt_toolkit >= 1.0.10
%else
Requires:	python-click => 3.2, python-pygments => 2.0
Requires:	python-sqlparse >= 0.1.14, python-%{name} >= 2.5.4
Requires:	python-jedi => 0.8.1 python-setproctitle >= 1.1.9
Requires:	python-wcwidth >= 0.1.6 python-humanize >= 0.5.1
Requires:	python-configobj >= 5.0.6 python-prompt_toolkit >= 1.0.10
%endif

%description
This is a PostgreSQL client that does auto-completion and syntax highlighting.

%if 0%{?fedora} && 0%{?rhel} >= 7
%package debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting (debug build)
# Require the base package, as we're sharing .py/.pyc files:
Requires:	%{name} = %{version}-%{release}

%description debug
This is a build of the for the debug build of Python 2.
%endif

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3

%description  -n python3-%{name}
This is a build of pgcli the for the Python 3.

%if 0%{?fedora} && 0%{?rhel} >= 7
%package -n python3-%{name}-debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3 (debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{name} = %{version}-%{release}

%description -n python3-%{name}-debug
This is a build of the pgcli for the debug build of Python 3.
%endif
%endif

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
%{_bindir}/%{name}
%dir %{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}/*
%{python2_sitelib}/*.egg-info/

%if 0%{?fedora} && 0%{?rhel} >= 7
%files debug
%defattr(-,root,root)
%doc LICENSE.txt
%endif

%if 0%{?with_python3}
%files -n python3-%{name}
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt DEVELOP.rst TODO
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/*.egg-info/

%if 0%{?fedora} && 0%{?rhel} >= 7
%files -n python3-%{name}-debug
%defattr(-,root,root)
%doc LICENSE
%endif
%endif

%changelog
* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Mon Sep 19 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix packaging errors, spec file errors, etc.

* Fri Apr 17 2015 Devrim Gündüz <devrim@gunduz.org> 0.16.3-1
- Initial packaging for PostgreSQL YUM repository.
