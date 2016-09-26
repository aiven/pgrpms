%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pgstat2

Summary:	PostgreSQL monitoring script
Name:		%{sname}_%{pgmajorversion}
Version:	1.01
Release:	3%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://download.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}/%{version}/%{sname}-%{version}.tar.gz
Source1:	README.%{sname}
URL:		http://pgfoundry.org/projects/%{sname}/
Requires:	postgresql%{pgmajorversion}-devel, python-psycopg2
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgstat is a command line utility to display PostgreSQL information on the
command line similar to iostat or vmstat. This data can be used for
monitoring or performance tuning.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}/
%{__install} -m 755 pgstat %{buildroot}%{_bindir}/
%{__cp} %{SOURCE1} README.%{sname}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.%{sname}
%{_bindir}/pgstat

%changelog
* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-3
- Update download URL
- Cosmetic updates to spec file

* Sat Oct 22 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.01-2
- Update layout for new PostgreSQL rpm layout.

* Wed Nov 25 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.01-1
- Update to 1.01

* Thu Mar 5 2009 - Devrim GUNDUZ <devrim@gunduz.org> 0.8beta-1
- Update to 0.8beta
- Add a README file -- tarball does not include one.

* Wed Feb 25 2009 - Devrim GUNDUZ <devrim@gunduz.org> 0.7beta-1
- Initial RPM packaging for yum.postgresql.org
