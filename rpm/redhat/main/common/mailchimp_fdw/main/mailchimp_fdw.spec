%global sname mailchimp_fdw
%global packagesoversion 0.3.0

%if 0%{?fedora} >= 35
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	PostgreSQL foreign data wrapper for Mailchimp
Name:		%{sname}
Version:	0.3.1
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/daamien/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/daamien/%{sname}

BuildArch:	noarch

%description
This is a PostgreSQL FDW for Mailchimp

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python3} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python_sitelib}/mailchimpfdw/
%{python_sitelib}/mailchimpfdw-%{packagesoversion}-py%{py3ver}.egg-info
%{python_sitelib}/mailchimpfdw/*.py*
%{python_sitelib}/mailchimpfdw/__pycache__/*.pyc

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-3PGDG
- Enable builds on Python 3.10+
- Add PGDG branding
- Minor spec file cleanup

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue May 16 2017 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-2
- Relax dependency on PostgreSQL.

* Wed Dec 30 2015 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Mon Mar 16 2015 - Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository

