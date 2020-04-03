%global debug_package %{nil}
%global __os_install_post %{nil}

Summary:	Fast data loader for PostgreSQL
Name:		pgloader
Version:	3.6.1
Release:	1%{?dist}
License:	BSD
URL:		http://pgloader.io
Source0:	https://github.com/dimitri/%{name}/releases/download/v%{version}/%{name}-bundle-%{version}.tgz

BuildRequires:	sbcl >= 1.3.6
BuildRequires:	freetds-devel
BuildRequires:	openssl-devel
Requires:	openssl-devel

%description
pgloader imports data from different kind of sources and COPY it into
PostgreSQL.

The command language is described in the manual page and allows to describe
where to find the data source, its format, and to describe data processing
and transformation.

Supported source formats include SQL Server, CSV, fixed width flat files,
dBase3 files (DBF), and SQLite and MySQL databases. In most of those formats,
pgloader is able to auto-discover the schema and create the tables and the
indexes in PostgreSQL. In the MySQL case it's possible to edit CASTing rules
from the pgloader command directly.

%prep
%setup -q -n %{name}-bundle-%{version}


%build
export CCFLAGS="%{_optflags}"
export CCXFLAGS="%{_optflags}"
export DYNSIZE=""
echo "Arch is : %{_arch}"
%if "%{_arch}" == "i386" || "%{_arch}" == "arm"
export DYNSIZE="DYNSIZE=1024"
%endif
%{__make} %{?_smp_mflags} ${DYNSIZE}
# TODO build doc with sphinx

%install
%{__rm} -rf %{buildroot}
%{__install} -m 755 -d %{buildroot}/%{_bindir}
%{__install} -m 755 bin/%{name} %{buildroot}%{_bindir}/pgloader

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.md
%{_bindir}/%{name}

%changelog
* Mon Jan 21 2019 Devrim Gündüz <devrim@gunduz.org> - 3.6.1-1
- Update to 3.6.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-1.1
- Rebuild against PostgreSQL 11.0

* Fri Sep 14 2018 Bruno Friedmann <bruno@ioda.net>  3.5.2-1
- Update to 3.5.2
- Cleanup unused deps (python)
- Adapt file list (no man.1)
- Use a proper build step

* Sun Feb 18 2018 Devrim Gündüz <devrim@gunduz.org> 3.4.3-1
- Add dependency to openssl-devel, per #3087

* Wed Jan 24 2018 Devrim Gündüz <devrim@gunduz.org> 3.4.2-1
- Rebuild (on RHEL 7 for now, for new SSL)

* Thu Jul 6 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.1-1
- Update to 3.4.1 (bundle release)

* Sat Dec 3 2016 Devrim Gündüz <devrim@gunduz.org> 3.3.2-1
- Update to 3.3.2 (bundle release)

* Mon Aug 29 2016 Devrim Gündüz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1 (bundle release)

* Tue Jul 28 2009 Devrim Gündüz <devrim@gunduz.org> 2.3.2-1
- Update to 2.3.2

* Sun Jun 15 2008 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1

* Wed Apr 9 2008 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Various spec file fixes

* Fri Feb 1 2008 Devrim Gündüz <devrim@gunduz.org> 2.2.6-1
- Update to 2.2.6

* Sat Jan 19 2008 Devrim Gündüz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5

* Thu Jun 21 2007 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Initial packaging
