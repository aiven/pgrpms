%global sname pg_catcheck

Summary:	Tool for diagnosing PostgreSQL system catalog corruption
Name:		%{sname}%{pgmajorversion}
Version:	1.1.0
Release:	1%{?dist}.2
License:	BSD
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_catcheck is a simple tool for diagnosing system catalog corruption.
If you suspect that your system catalogs are corrupted, this tool may
help you figure out exactly what problems you have and how serious they
are. If you are paranoid, you can run it routinely to search for system
catalog corruption that might otherwise go undetected. However, pg_catcheck
is not a general corruption detector. For that, you should use PostgreSQL's
checksum feature (`initdb -k`).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/%{sname}
%{pginstdir}/doc/README-%{sname}.md

%changelog
* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Dec 12 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0
* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
