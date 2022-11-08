%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname pyrseas
%global cname Pyrseas

Summary:	Compare and synchronize PostgreSQL database schemas
Name:		python3-%{sname}
Version:	0.10.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/perseas/%{cname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/perseas/%{cname}/
BuildArch:	noarch

Requires:	python3-pgdbconn
Obsoletes:	python2-%{sname} <= 0.9.0

%description
Pyrseas provides a framework and utilities to upgrade and maintain a relational
database. Its purpose is to enhance and follow through on the concepts of the
Andromeda Project. This is Python 3 version.

%prep
%setup -q -n %{cname}-%{version}

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
%{_bindir}/dbaugment
%{_bindir}/dbtoyaml
%{_bindir}/yamltodb
%{python3_sitelib}/%{cname}-%{version}-py%{py3ver}*.egg-info/*
%{python3_sitelib}/%{sname}

%changelog
* Tue Nov 8 2022 - Devrim Gündüz <devrim@gunduz.org> 0.10.0-1
- Update to 0.10.0

* Thu Apr 16 2020 - Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1
- Remove Python2 stuff

* Fri Jul 26 2019 - Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Update to 0.9.0
- Add dbpgconn dependency

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Update to 0.8.0

* Tue Nov 29 2016 - Devrim Gündüz <devrim@gunduz.org> 0.7.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
