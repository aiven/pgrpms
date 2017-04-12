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

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global	sname	pyrsistent

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Summary:	Persistent/Functional/Immutable data structures
Version:	0.11.13
Release:	3%{dist}
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
URL:		http://github.com/tobgu/pyrsistent/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{sname}}
%{?python_provide:%python_provide python3-flask-sqlalchemy}
BuildRequires:	python3-devel
Requires:	python3-six
%else
BuildRequires:	python-devel
Requires:	python-six
%endif # with_python3

%description
Pyrsistent is a number of persistent collections (by some referred to
as functional data structures). Persistent in the sense that they are
immutable.

%prep
%setup -q -n %{sname}-%{version}

# Remove bundled egg-info
%{__rm} -r %{sname}.egg-info

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%if 0%{?with_python3}
%{__ospython3} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/__pycache__/*%{sname}* %{buildroot}%{python3_sitearch}/_%{sname}_version.py %{buildroot}%{python3_sitearch}/pvectorc.cpython*  %{buildroot}%{python3_sitearch}/%{sname}-%{version}-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname}* %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/_%{sname}_version.py* %{buildroot}%{python2_sitearch}/pvectorc.* %{buildroot}/%{pgadmin4py2instdir}
%endif # with_python3

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.rst
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%dir %{pgadmin4py3instdir}/%{sname}
%{pgadmin4py3instdir}/%{sname}/*
%{pgadmin4py3instdir}/__pycache__/*%{sname}*
%{pgadmin4py3instdir}/_%{sname}*
%{pgadmin4py3instdir}/pvectorc*.so
%else
%dir %{pgadmin4py2instdir}/%{sname}
%{pgadmin4py2instdir}/%{sname}/*
%{pgadmin4py2instdir}/_%{sname}*
%{pgadmin4py2instdir}/%{sname}*egg-info/
%{pgadmin4py2instdir}/pvectorc*.so
%endif

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> 0.11.13-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-2
- Fix packaging errors, that would own /usr/lib64 or so.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.


