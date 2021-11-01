
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Summary:	MySQL to PostgreSQL replica system
Name:		pg_chameleon
Version:	2.0.16
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/the4thdoctor/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/the4thdoctor/%{name}
BuildArch:	noarch

Requires:	python3-PyMySQL python3-psycopg2 python3-rollbar
Requires:	python3-mysql-replication python3-tabulate python3-daemonize
%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	python36-PyYAML
%else
Requires:	python3-pyyaml
%endif

%description
pg_chameleon is a MySQL to PostgreSQL replica system written in Python 3.
The system use the library mysql-replication to pull the row images from
MySQL which are stored into PostgreSQL as JSONB. A pl/pgsql function decodes
the jsonb values and replays the changes against the PostgreSQL database.

%prep
%setup -q -n %{name}-%{version}

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
%license LICENSE.txt
%{_bindir}/chameleon
%{_bindir}/chameleon.py
%{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}/configuration/config-example.yml
%{python3_sitelib}/%{name}/lib/*.py
%{python3_sitelib}/%{name}/lib/__pycache__/*.pyc
%{python3_sitelib}/%{name}/sql/*.sql
%{python3_sitelib}/%{name}/sql/upgrade/*.sql

%changelog
* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-3
- Looks like we don't need python3-sphinx dependency.

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-2
- Fix RHEL 7 dependency

* Wed Dec 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-1
- Update to 2.0.16

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.15-1
- Update to 2.0.15

* Tue Aug 18 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.14-1
- Initial RPM packaging for PostgreSQL RPM Repository
