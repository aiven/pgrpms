Name:		MigrationWizard
Version:        1.1
Release:        3%{?dist}.2
Summary:	MySQL to PostgreSQL Migration Wizard

License:	BSD
URL:		https://www.enterprisedb.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-jdk-version.patch

BuildArch:	noarch

BuildRequires:	ant
Requires:	java

%description
This is MySQL to PostgreSQL Migration Wizard by EnterpriseDB.

%prep
%setup -q -n wizard
%patch -P 0 -p0

%build
ant compile

%install
%{__rm} -rf %{buildroot}
ant dist
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -d %{buildroot}%{_datadir}/%{name}/lib
%{__install} -m 644 dist/*.jar %{buildroot}%{_datadir}/%{name}
%{__install} -m 644 dist/lib/* %{buildroot}%{_datadir}/%{name}/lib

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_datadir}/%{name}/lib/*

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-3.2
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1-3.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gunduz <devrim@gunduz.org> 1.1-3
- Update patch for recent distros.

* Thu Jan 10 2013 Devrim Gunduz <devrim@gunduz.org> 1.1-2
- Add a patch to compile on Fedora 17 (jdk 1.7)

* Wed Oct 28 2009 Devrim Gunduz <devrim@gunduz.org> 1.1-1
- Initial build for PostgreSQL RPM Repository
