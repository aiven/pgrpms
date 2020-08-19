%global debug_package %{nil}

%global sname mailchimp_fdw
%global packagesoversion 0.3.0

%global __ospython %{_bindir}/python3
%{expand: %%global pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	PostgreSQL foreign data wrapper for Mailchimp
Name:		%{sname}
Version:	0.3.1
Release:	2%{?dist}.1
License:	BSD
Source0:	https://github.com/daamien/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/daamien/mailchimp_fdw

%description
This is a PostgreSQL FDW for Mailchimp

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python_sitelib}/mailchimpfdw/
%{python_sitelib}/mailchimpfdw-%{packagesoversion}-py%{pybasever}.egg-info
%{python_sitelib}/mailchimpfdw/*.py*
%if 0%{?fedora} && 0%{fedora} >= 31
%{python_sitelib}/mailchimpfdw/__pycache__/*.pyc
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue May 16 2017 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-2
- Relax dependency on PostgreSQL.

* Wed Dec 30 2015 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Mon Mar 16 2015 - Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository

