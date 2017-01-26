%global debug_package %{nil}
%global pgmajorversion 9.5
%global pginstdir /usr/pgsql-95
%global sname powa
%global swebname powa-web
# Powa version
%global powamajorversion 3
%global powamidversion 1
%global powaminorversion 0
# powa-web version
%global powawebversion 3.1.0

%global	powawebdir  %{_datadir}/%{name}

%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL Workload Analyzer
Name:		%{sname}_%{pgmajorversion}
Version:	%{powamajorversion}.%{powamidversion}.%{powaminorversion}
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dalibo/powa-archivist/archive/REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}.zip
Source1:	https://github.com/dalibo/%{swebname}/archive/%{powawebversion}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		http://dalibo.github.io/powa/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-contrib
# Actually these are optional, but let's add them for a better PoWA instance.
Requires:	pg_qualstats%{pgmajorversion}, pg_stat_kcache%{pgmajorversion}
Requires:	hypopg_%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

%package web
Summary:	The user interface of powa
Group:		Applications/Databases
BuildRequires:	python-setuptools
Requires:	python-tornado >= 2.0, python-psycopg2, python-sqlalchemy

%description web
This is the user interface of POWA.

%prep
%setup -q -n %{sname}-archivist-REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}
%patch0 -p0

%build
make %{?_smp_mflags}

# Build powa-web
tar zxf %{SOURCE1}
pushd %{swebname}-%{powawebversion}
%{__python} setup.py build
popd

%install
%{__rm} -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
# Move powa docs into their own subdirectory:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/%{sname}
%{__mv} %{buildroot}%{pginstdir}/doc/extension/*.md %{buildroot}%{pginstdir}/doc/extension/%{sname}

# Install powa-web
pushd %{swebname}-%{powawebversion}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{pginstdir}/doc/extension/%{sname}
%doc %{pginstdir}/doc/extension/%{sname}/*.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%files web
%defattr(-,root,root,-)
%{_bindir}/%{swebname}
%dir %{python_sitelib}/%{sname}
%{python_sitelib}/%{sname}/*
%{python_sitelib}/powa_web-%{powawebversion}-py%{pyver}.egg-info/*

%changelog
* Wed Jan 25 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-2
- Fix dependencies, per patch from Thomas Reiss. Per #2072.
- Add dependency for hypopg, per #2073.

* Fri Oct 28 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-1
- Update both components to 3.1.0

* Wed Feb 10 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Wed Jan 27 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0
- Improve spec file, to fix multiple issues.

* Mon Jan 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1
- Fix a stupid oversight in spec file: This package contains
  3 digit version number.

* Tue Oct 28 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Wed Aug 27 2014 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
