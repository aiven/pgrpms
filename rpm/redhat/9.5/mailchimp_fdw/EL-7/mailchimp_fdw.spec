%global debug_package %{nil}

%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname mailchimp_fdw
%global packagesoversion 0.3.0

#Python major version.
%{expand: %%global pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL foreign data wrapper for Mailchimp
Name:		%{sname}%{pgmajorversion}
Version:	0.3.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/daamien/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/daamien/mailchimp_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a PostgreSQL FDW for Mailchimp

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python_sitelib}/mailchimpfdw/
%{python_sitelib}/mailchimpfdw-%{packagesoversion}-py%{pybasever}.egg-info
%{python_sitelib}/mailchimpfdw/*.py*

%changelog
* Wed Dec 30 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Mon Mar 16 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository

