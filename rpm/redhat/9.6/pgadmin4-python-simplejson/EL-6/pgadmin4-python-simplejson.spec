%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

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

Name:           python-simplejson

Version:        3.8.2
Release:        1%{?dist}
Summary:        Simple, fast, extensible JSON encoder/decoder for Python

Group:          System Environment/Libraries
# The main code is licensed MIT.
# The docs include jquery which is licensed MIT or GPLv2
License: (MIT or AFL) and (MIT or GPLv2)
URL:            http://undefined.org/python/#simplejson
Source0:        http://pypi.python.org/packages/source/s/simplejson/simplejson-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires: python-sphinx
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-nose
%endif # with_python3

# we don't want to provide private python extension libs
%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch}).*\\.so$


%description
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.5+. It is pure Python code
with no dependencies, but includes an optional C extension for a serious speed
boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.5.  It gets updated more regularly than the json module in the
python stdlib.

%if 0%{?with_python3}
%package -n python3-simplejson
Summary:        Simple, fast, extensible JSON encoder/decoder for Python3
Group:          System Environment/Libraries

%description -n python3-simplejson
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.5+ and python3.3+ It is pure
Python code with no dependencies, but includes an optional C extension for a
serious speed boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.5.  It gets updated more regularly than the json module in the
python stdlib.

%endif # with_python3

%prep
%setup -q -n simplejson-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif # with_python3

%build
%{__ospython2} setup.py build
./scripts/make_docs.py

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif # with_python3

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root=%{buildroot}

%{__rm} docs/.buildinfo
%{__rm} docs/.nojekyll

%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root=%{buildroot}
%endif # with_python3

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs LICENSE.txt
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-simplejson
%defattr(-,root,root,-)
%doc LICENSE.txt
%{python3_sitearch}/*
%endif # python3

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 3.8.2-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
