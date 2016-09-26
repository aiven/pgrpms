Summary:	PostgreSQL monitoring script
Name:		check_postgres
Version:	2.22.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}-%{version}.tar.gz
URL:		http://bucardo.org/wiki/Check_postgres
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
check_postgres is a script for monitoring various attributes of your
database. It is designed to work with Nagios, MRTG, or in standalone
scripts.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{_libdir}/perl5/vendor_perl/5.8.8/i386-linux-thread-multi/auto/%{name}/.packlist

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{name}.pl.html README TODO
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}.pl

%changelog
* Sun Jul 5 2015 - Devrim GUNDUZ <devrim@gunduz.org> 2.22.0-1
- Update to 2.22.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2015-July/000035.html
- Update description

* Wed Oct 9 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.21.0-1
- Update to 2.21.0
- Simplify spec file.

* Tue Jul 2 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.20.1-1
- Update to 2.20.1

* Mon Apr 29 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.20.0-1
- Update to 2.20.0

* Sun Feb 26 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.19.0-1
- Update to 2.19.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2012-January/000028.html

* Sun Oct 2 2011 - Devrim GUNDUZ <devrim@gunduz.org> 2.18.0-1
- Update to 2.18.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2011-October/000027.html

* Fri Jan 28 2011 - Devrim GUNDUZ <devrim@gunduz.org> 2.16.0-1
- Update to 2.16.0

* Mon Jan 10 2011 - Devrim GUNDUZ <devrim@gunduz.org> 2.15.4-1
- Update to 2.15.4

* Wed Mar 10 2010 - Devrim GUNDUZ <devrim@gunduz.org> 2.14.3-1
- Update to 2.14.3

* Sat Feb 27 2010 - Devrim GUNDUZ <devrim@gunduz.org> 2.14.2-1
- Update to 2.14.2
- Add -p options to install, per bz review #543917, comment #3.
- Remove postgresql-server requirement, since this plugin can be used to
  control remote PostgreSQL servers.

* Mon Feb 1 2010 - Devrim GUNDUZ <devrim@gunduz.org> 2.13.0-1
- Update to 2.13.0
- Refactor spec file:
  * Use tarball, instead of .pl file directly.
  * Add man page

* Wed Sep 2 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.12.0-1
- Update to 2.12.0

* Wed Sep 2 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.11.1-1
- Update to 2.11.1

* Tue Aug 4 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.9.10-1
- Update to 2.9.10

* Tue Jul 28 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.9.2-1
- Update to 2.9.2

* Sat Jul 4 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.9.1-1
- Update to 2.9.1

* Mon May 18 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.8.1-1
- Update to 2.8.1

* Thu May 7 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.8.0-1
- Update to 2.8.0

* Tue Feb 17 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Sun Feb 1 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.6.0-1
- Update to 2.6.0

* Fri Dec 19 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.5.3-1
- Update to 2.5.3

* Wed Dec 17 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.5.2-1
- Update to 2.5.2

* Sun Dec 7 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.5.0-1
- Update to 2.5.0

* Tue Dec 2 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.4.3-1
- Update to 2.4.3

* Tue Oct 7 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Make package noarch

* Mon Sep 29 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Tue Sep 23 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.4-1
- Initial RPM packaging for yum.postgresql.org
