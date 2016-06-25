%global sname check_pgactivity
%global pgmajorversion 94

%global		_tag REL1_25

Name:		nagios-plugins-pgactivity
Version:	1.25
Release:	1
Summary:	PostgreSQL monitoring plugin for Nagios
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://opm.io
Source0:	https://github.com/OPMDG/%{sname}/archive/%{_tag}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	postgresql%{pgmajorversion}
Requires:	nagios-plugins
Provides:	%{sname} = %{version}

%description
check_pgactivity is a monitoring plugin of PostgreSQL for Nagios. It provides
many checks and allow the gathering of many performance counters.
check_pgactivity is part of Open PostgreSQL Monitoring.

%prep
%setup -q -n %{sname}-%{_tag}

%build

%install
install -D -p -m 0755 %{sname} %{buildroot}/%{_libdir}/nagios/plugins/%{sname}

%files
%defattr(-,root,root,0755)
%{_libdir}/nagios/plugins/%{sname}
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.rst LICENSE
%else
%doc README.rst
%license LICENSE
%endif

%changelog
* Wed Feb 10 2016 Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Update to 1.25

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.25-beta1-1
- Update to 1.25 beta1
- Fix rpmlint warnings, and adjust to PGDG release format.

* Wed Dec 10 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.19-1
- update to release 1.19

* Fri Sep 19 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.15-1
- Initial version

