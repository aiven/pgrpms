%global __python %{_bindir}/python3
%global sname powa-web
%global swebname powa

%global	powawebdir  %{_datadir}/%{name}

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	The user interface of PoWA
Name:		%{sname}
Version:	4.2.0
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-web/archive/refs/tags/%{version}.tar.gz
URL:		https://powa.readthedocs.io/
Requires:	python3-tornado python3-sqlalchemy
BuildRequires:	pgdg-srpm-macros
BuildArch:	noarch

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

This is the user interface of POWA.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# Install sample conf file
%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__install} powa-web.conf-dist %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root,-)
%{_bindir}/%{sname}
%dir %{python_sitelib}/%{swebname}
%{python_sitelib}/%{swebname}/*
%{python_sitelib}/powa_web-%{version}-py%{pyver}.egg-info/*
%{_sysconfdir}/powa-web.conf-dist

%changelog
* Wed Sep 20 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1PGDG
- Update to 4.2.0
- Trim changelog
