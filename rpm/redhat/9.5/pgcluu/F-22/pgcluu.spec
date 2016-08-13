Summary:	PostgreSQL performance monitoring and auditing tool
Name:		pgcluu
Version:	2.5
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
URL:		http://pgcluu.darold.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

%description
gCluu is a PostgreSQL performances monitoring and auditing tool.
View reports of all statistics collected from your PostgreSQL
databases cluster. pgCluu will show you the entire information
of the PostgreSQL cluster and the system utilization

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}_collectd
%perl_vendorarch/auto/pgCluu/.packlist
%{_mandir}/man1/%{name}.1.gz

%changelog
* Sat Aug 13 2016 Devrim GÜNDÜZ <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Sep 11 2015 Devrim GÜNDÜZ <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Fix rpmlint warning (add %%build section)
- Update download URL

* Sun Jan 11 2015 Devrim GÜNDÜZ <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Fri Sep 26 2014 Devrim GÜNDÜZ <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Tue Apr 1 2014 Devrim GÜNDÜZ <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Wed Jan 15 2014 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
