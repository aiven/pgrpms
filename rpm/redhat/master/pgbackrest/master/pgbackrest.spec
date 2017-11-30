%global debug_package %{nil}
Summary:	Reliable PostgreSQL Backup & Restore
Name:		pgbackrest
Version:	1.26
Release:	1%{?dist}
License:	MIT
Group:		Applications/Databases
Url:		http://www.pgbackrest.org/
Source0:	https://github.com/pgbackrest/pgbackrest/archive/release/%{version}.tar.gz
Source1:	pgbackrest-conf.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildArch:	noarch
Requires:	perl-XML-LibXML perl-IO-Socket-SSL
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
pgBackRest aims to be a simple, reliable backup and restore system that can
seamlessly scale up to the largest databases and workloads.

Instead of relying on traditional backup tools like tar and rsync, pgBackRest
implements all backup features internally and uses a custom protocol for
communicating with remote systems. Removing reliance on tar and rsync allows
for better solutions to database-specific backup challenges. The custom remote
protocol allows for more flexibility and limits the types of connections that
are required to perform a backup which increases security.

%prep
%setup -q -n %{name}-release-%{version}

%build
pushd libc
perl Makefile.PL INSTALL_BASE=%{buildroot}/usr
%{__make}
popd

%install
%{__install} -D -d -m 0755 %{buildroot}%{perl_vendorlib} %{buildroot}%{_bindir}
%{__install} -D -d -m 0700 %{buildroot}/%{_sharedstatedir}/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/log/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/spool/%{name}
%{__install} -D -d -m 0755 %{buildroot}%{_sysconfdir}
%{__install} %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf
%{__cp} -a lib/* %{buildroot}%{perl_vendorlib}/
%{__cp} -a bin/%{name} %{buildroot}%{_bindir}/%{name}

pushd libc
%{__make} install
popd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{_bindir}/%{name}
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{name}.conf
%{perl_vendorlib}/pgBackRest/
%attr(-,postgres,postgres) /var/log/%{name}
%attr(-,postgres,postgres) %{_sharedstatedir}/%{name}
%attr(-,postgres,postgres) /var/spool/%{name}
/usr/lib/perl5/x86_64-linux-thread-multi/auto/pgBackRest/LibC/.packlist
/usr/lib/perl5/x86_64-linux-thread-multi/auto/pgBackRest/LibC/LibC.so
/usr/lib/perl5/x86_64-linux-thread-multi/auto/pgBackRest/LibC/autosplit.ix
/usr/lib/perl5/x86_64-linux-thread-multi/perllocal.pod
/usr/lib/perl5/x86_64-linux-thread-multi/pgBackRest/LibC.pm
/usr/lib/perl5/x86_64-linux-thread-multi/pgBackRest/LibCAuto.pm

%changelog
* Sun Nov 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.26-1
- Update to 1.26, per #2889
- Add perl-libc related files.

* Thu Oct 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Update to 1.25, per #2823

* Sun Oct 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.24-1
- Update to 1.24, per #2743

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.23-1
- Update to 1.23, per #2675.

* Thu Aug 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.22-1
- Update to 1.22, per #2643.

* Thu Jun 29 2017 - Devrim Gündüz <devrim@gunduz.org> 1.20-1
- Update to 1.20, per #2517.

* Tue Jun 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.19-1
- Update to 1.19, per #2483.

* Wed May 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.18-1
- Update to 1.18

* Tue Mar 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.17-1
- Update to 1.17

* Fri Mar 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.16-1
- Update to 1.16

* Wed Feb 8 2017 - Devrim Gündüz <devrim@gunduz.org> 1.13-1
- Update to 1.13

* Thu Dec 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.12-1
- Update to 1.12

* Thu Nov 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.11-1
- Update to 1.11

* Tue Nov 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.10-1
- Update to 1.10

* Thu Nov 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Update to 1.09
- Install default conf file, per David Steele.
- Install default directories, per David Steele.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.08-1
- Update to 1.08

* Fri Aug 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Fri May 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial packaging for PostgreSQL RPM Repository

