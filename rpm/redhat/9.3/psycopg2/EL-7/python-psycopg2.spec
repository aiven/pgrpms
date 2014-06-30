# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname psycopg2

Summary:	A PostgreSQL database adapter for Python
Name:		python-%{sname}
Version:	2.5.3
Release:	1%{?dist}
Source0:	http://initd.org/psycopg/tarballs/PSYCOPG-2-5/%{sname}-%{version}.tar.gz
Patch0:		setup.cfg.patch
License:	GPL (with Exceptions)
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://www.psycopg.org/psycopg/
BuildRequires:	python-devel postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-libs

Obsoletes:	python-psycopg2-zope <= 2.0.5.1-8

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch 
with the aim of being very small and fast, and stable as a rock. The 
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%package test
Summary:	Tests for psycopg2
Group:		Development Libraries
Requires:	%{name} = %{version}-%{release}

%description test
Tests for psycopg2.

%prep
%setup -q -n psycopg2-%{version}
%patch0 -p0

%build
python setup.py build
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}%{python_sitearch}/psycopg2
python setup.py install --no-compile --root %{buildroot}

#install -d %{buildroot}%{ZPsycopgDAdir}
#cp -pr ZPsycopgDA/* %{buildroot}%{ZPsycopgDAdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL LICENSE README NEWS
%dir %{python_sitearch}/psycopg2
%{python_sitearch}/psycopg2/*.py
%{python_sitearch}/psycopg2/*.pyc
%{python_sitearch}/psycopg2/*.so
%{python_sitearch}/psycopg2/*.pyo
%{python_sitearch}/psycopg2-%{version}-py%{pyver}.egg-info

%files test
%defattr(-,root,root)
%{python_sitearch}/%{sname}/tests/*

%files doc
%defattr(-,root,root)
%doc doc examples/

%changelog
* Mon May 19 2014 Devrim Gündüz <devrim@gunduz.org> 2.5.3-1
- Update to 2.5.3, per changes described at:
  http://www.psycopg.org/psycopg/articles/2014/05/13/psycopg-253-released 
- Trim changelog

* Tue Jan 7 2014 Devrim Gündüz <devrim@gunduz.org> 2.5.2-1
- Update to 2.5.2, per changes described at:
  http://www.psycopg.org/psycopg/articles/2014/01/07/psycopg-252-released

* Sun Jun 30 2013 Devrim GUNDUZ <devrim@gunduz.org> 2.5.1-1
- Update to 2.5.1, per changes described at:
  http://www.psycopg.org/psycopg/articles/2013/06/23/psycopg-251-released/

* Thu Apr 11 2013 Devrim GUNDUZ <devrim@gunduz.org> 2.5-1
- Update to 2.5, per changes described at:
  http://www.psycopg.org/psycopg/articles/2013/04/07/psycopg-25-released/
