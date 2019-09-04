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

%global sname	pgdbconn

Summary:	Object-oriented layer over Psycopg2 to connect and interact with Postgres databases
Name:		python2-%{sname}
Version:	0.8.0
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/perseas/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/perseas/%{sname}/
BuildArch:	noarch

%description
PgDbConn is an offshoot from the Perseas project (started as Pyrseas) to
isolate and generalize the Postgres database connection code so that it can
be used in other Perseas products, such as a web application to update
Postgres tables.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:	Object-oriented layer over Psycopg2 to connect and interact with Postgres databases

%description -n python3-%{sname}
PgDbConn is an offshoot from the Perseas project (started as Pyrseas) to
isolate and generalize the Postgres database connection code so that it can
be used in other Perseas products, such as a web application to update
Postgres tables. This is Python 3 version.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --root %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install --root %{buildroot}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}*.egg-info/*
%{python2_sitelib}/%{sname}

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc docs/ README.rst
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}*.egg-info/*
%{python3_sitelib}/%{sname}
%endif

%changelog
* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-2
- Fix OS versions in Makefile, the distro name in the packages changed.

* Fri Jul 26 2019 - Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Initial RPM packaging for PostgreSQL RPM Repository to satisfy
  pyrseas dependency.
