%global sname simplejson

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

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif

Version:	3.16.0
Release:	1%{?dist}
Summary:	Simple, fast, extensible JSON encoder/decoder for Python
Group:		System Environment/Libraries
# The main code is licensed MIT.
# The docs include jquery which is licensed MIT or GPLv2
License:	(MIT or AFL) and (MIT or GPLv2)
URL:		http://undefined.org/python/#simplejson
Source0:	https://files.pythonhosted.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
%if 0%{?rhel} == 6
Patch0:		pgadmin4-python-simplejson-rhel6-sphinx.patch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel
%endif
%endif

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools python3-nose python3-sphinx
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname} < %{version}
BuildRequires:	python34-devel python34-setuptools python34-nose python-sphinx10
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools python-nose python-sphinx
%endif

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

%prep
%setup -q -n simplejson-%{version}
%if 0%{?rhel} == 6
%patch0 -p0
%endif

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif # with_python3

%build
%{__ospython} setup.py build
./scripts/make_docs.py

%install
%{__rm} -rf %{buildroot}

%{__ospython} setup.py install --skip-build --root=%{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}/%{sname}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname}/* %{buildroot}/%{pgadmin4py3instdir}/%{sname}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname}*egg* %{buildroot}/%{pgadmin4py3instdir}/
%else # Python 2
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}/%{sname}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname}/* %{buildroot}/%{pgadmin4py2instdir}/%{sname}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname}*egg* %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3

%{__rm} docs/.buildinfo
%{__rm} docs/.nojekyll

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs LICENSE.txt
%if 0%{?with_python3}
%dir %{pgadmin4py3instdir}/%{sname}/
%{pgadmin4py3instdir}/%{sname}/*
%{pgadmin4py3instdir}/%{sname}*egg*
%else # Python 2
%doc docs LICENSE.txt
%dir %{pgadmin4py2instdir}/%{sname}/
%{pgadmin4py2instdir}/%{sname}/*
%{pgadmin4py2instdir}/%{sname}*egg*
%endif # python3

%changelog
* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 3.16.0-1
- Update to 3.16.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.13.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 3.13.2-1
- Update to 3.13.2

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 3.8.2-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 3.8.2-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 3.8.2-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
