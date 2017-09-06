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

%global sname	flask-paranoid
%global mod_name	Flask-Paranoid

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif

Version:	0.1
Release:	1%{?dist}
Summary:	Simple user session protection
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{mod_name}/
Source0:	https://github.com/miguelgrinberg/flask-paranoid/archive/v0.1.tar.gz
BuildArch:	noarch

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{sname}}
%else
%{?python_provide:%python_provide python-%{sname}}
%endif

%description
Simple user session protection.

%prep
%setup -q -n %{sname}-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/Flask_Paranoid* %{buildroot}%{python3_sitelib}/flask_paranoid %{buildroot}/%{pgadmin4py3instdir}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/Flask_Paranoid* %{buildroot}%{python2_sitelib}/flask_paranoid %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc LICENSE README.md
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Flask_Paranoid*.egg-info/
%dir %{pgadmin4py3instdir}/flask_paranoid
%{pgadmin4py3instdir}/flask_paranoid/*
%else
%{pgadmin4py2instdir}/Flask_Paranoid*.egg-info/
%dir %{pgadmin4py2instdir}/flask_paranoid
%{pgadmin4py2instdir}/flask_paranoid/*
%endif

%changelog
* Wed Sep 6 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-1
- Initial packaging to satisfy pgadmin4 2.0 dependencies
