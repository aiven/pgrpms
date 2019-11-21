Summary:	Bloat check script for PostgreSQL
Name:		pg_bloat_check
Version:	2.6.1
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/keithf4/%{name}/archive/v%{version}.tar.gz
Source1:	%{name}-LICENSE
URL:		https://github.com/keithf4/%{name}
BuildArch:	noarch

Requires:	python3-psycopg2

%description
Script to provide a bloat report for PostgreSQL tables and/or indexes.
Requires at least Python 2.6 and the pgstattuple contrib module.

%prep
%setup -q

%build
%{__cp} %{SOURCE1} ./LICENSE
%install
%{__rm} -rf %{buildroot}

# Change /usr/bin/python to /usr/bin/python3 in the scripts:
sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" pg_bloat_check.py

%{__install} -d -m 755 %{buildroot}%{_bindir}
%{__install} -m 755 %{name}.py %{buildroot}%{_bindir}/

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md CHANGELOG LICENSE
%else
%doc README.md CHANGELOG
%license LICENSE
%endif
%attr(755,root,root) %{_bindir}/%{name}.py

%changelog
* Sat Nov 9 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1
- Switch to Python3

* Thu Jul 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
- Update to 2.5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.3-2.1
- Rebuild against PostgreSQL 11.0

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4.3-2
- Require python-psycopg2

* Thu Feb 15 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4.3-1
- Update to 2.4.3

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.5-1
- Update to 2.3.5

* Sun Feb 26 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.3-1
- Update to 2.3.3

* Sun Aug 7 2016 - Devrim Gündüz <devrim@gunduz.org> 2.3.2-1
- Update to 2.3.2

* Fri Jul 15 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
