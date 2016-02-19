# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname PyGreSQL

Summary:	Development module for Python code to access a PostgreSQL DB
Name:		postgresql%{pgmajorversion}-python
Version:	4.2
Release:	1PGDG%{?dist}
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://www.pygresql.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	https://pypi.python.org/packages/source/P/%{sname}/%{sname}-%{version}.zip
Patch0:		setup.py-rpm.patch

BuildRequires:	python-devel, postgresql%{pgmajorversion}-devel
Requires:	python, postgresql%{pgmajorversion}-libs

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs/*
%{python_sitearch}/*.so
%attr (755,root,root) %{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%dir %{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info
%{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info/*

%changelog
* Fri Feb 19 2016 Devrim Gündüz <devrim@gunduz.org> 0:4.2.1-1PGDG
- Update to 4.2.1
- Fix rpmlint warnings, update patch, clean up some macros.

* Wed Sep 9 2015 Devrim Gunduz <devrim@gunduz.org> 0:4.1.1-2PGDG
- Remove dependency of mx, per Jimmy Angelakos.

* Tue Jan 15 2013 Devrim Gunduz <devrim@gunduz.org> 0:4.1.1-1PGDG
- Update to 4.1.1

* Tue Oct 12 2010 Devrim Gunduz <devrim@gunduz.org> 0:4.0-2PGDG
- Apply 9.0 specific changes to spec file

* Thu Jan 1 2009 Devrim Gunduz <devrim@gunduz.org> 0:4.0-1PGDG
- Update to 4.0

* Fri Jan 4 2008 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-7PGDG
- Add postgresql-libs as Requires
- Use a more proper Requires and Release info

* Tue Jan 1 2008 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-6PGDG
- Added postgresql-devel as buildrequires
- Changed buildroot macro
- Fix dist macro

* Mon Sep 3 2007 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-5PGDG
- Add {?dist} to release tag.

* Sun Dec 3 2006 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-4PGDG
- Rebuilt

* Wed Aug 16 2006 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-3PGDG
- Rebuilt for PostgreSQL 8.2 RPM Set

* Mon Jul 17 2006 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-2PGDG
- Rebuilt for PostgreSQL 8.1

* Mon Jul 10 2006 Devrim Gunduz <devrim@gunduz.org> 0:3.8.1-1PGDG
- Initial build for PGDG RPM Set
