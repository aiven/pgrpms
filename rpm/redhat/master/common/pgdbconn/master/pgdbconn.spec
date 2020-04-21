%global sname	pgdbconn

%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Summary:	Object-oriented layer over Psycopg2 to connect and interact with Postgres databases
Name:		python3-%{sname}
Version:	0.8.0
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/perseas/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/perseas/%{sname}/
BuildArch:	noarch

Obsoletes:	python2-%{sname} <= 0.8.0-2

%description
PgDbConn is an offshoot from the Perseas project (started as Pyrseas) to
isolate and generalize the Postgres database connection code so that it can
be used in other Perseas products, such as a web application to update
Postgres tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython3} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython3} setup.py install --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}*.egg-info/*
%{python3_sitelib}/%{sname}

%changelog
* Tue Apr 21 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-3
- Retire PY2 package.

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-2
- Fix OS versions in Makefile, the distro name in the packages changed.

* Fri Jul 26 2019 - Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Initial RPM packaging for PostgreSQL RPM Repository to satisfy
  pyrseas dependency.
