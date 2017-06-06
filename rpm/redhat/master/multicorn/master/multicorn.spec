%global sname multicorn
%if 0%{?fedora} > 21
%global with_python3 1
%endif

%if 0%{?with_python3}
%global python_runtimes python python-debug python3 python3-debug
%else
%global python_runtimes python
%endif # with_python3

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?with_python3}
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%endif # with_python3

Summary:	Multicorn Python bindings for Postgres 9.2+ FDW
Name:		%{sname}%{pgmajorversion}
Version:	1.3.3
Release:	1%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/multicorn/
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python-devel
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-debug
%endif # with_python3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Multicorn Foreign Data Wrapper allows you to write foreign data wrappers
in python.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}.so
%dir %{python_sitearch}/%{sname}/
%{python_sitearch}/%{sname}/*
%dir %{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info
%{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info/*

%changelog
* Mon Mar 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3, per #2224 .

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Thu Dec 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4

* Wed Jan 21 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.3-1
- Initial packaging for PostgreSQL RPM Repository
