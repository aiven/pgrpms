%global	debug_package %{nil}
%{expand: %%global pyver %(echo `%__python3 -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global	python3_sitelib %(%__python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	Continuous Archiving for Postgres
Name:		wal-e
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/%{name}/%{name}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python3-devel
Requires:	python3-gevent => 1.1.1

%description
WAL-E is a program designed to perform continuous archiving of PostgreSQL
WAL files and base backups.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%__python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{python3_sitelib}/wal_e/
%{_bindir}/%{name}
%{python3_sitelib}/wal_e-%{version}-py%{pyver}.egg-info/*

%changelog
* Mon Nov 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
