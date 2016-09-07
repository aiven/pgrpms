Summary:	A fast PostgreSQL log analyzer
Name:		pgbadger
Version:	9.0
Release:	1%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
Source0:	https://github.com/dalibo/%{name}/archive/v%{version}.tar.gz
URL:		http://dalibo.github.com/pgbadger/
BuildArch:	noarch

%description
pgBadger is a PostgreSQL log analyzer build for speed with fully
detailed reports from your PostgreSQL log file. It's a single and small
Perl script that aims to replace and outperform the old php script
pgFouine.

pgBadger is written in pure Perl language. It uses a javascript library
to draw graphs so that you don't need additional Perl modules or any
other package to install. Furthermore, this library gives us more
features such as zooming.

pgBadger is able to autodetect your log file format (syslog, stderr or
csvlog). It is designed to parse huge log files as well as gzip
compressed file.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
# Remove .packlist file (per rpmlint)
%{__rm} -f %{buildroot}/%perl_vendorarch/auto/pgBadger/.packlist

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README LICENSE
%else
%doc README
%license LICENSE
%endif
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1p.gz

%changelog
* Wed Sep 7 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 9.0-1
- Update to 9.0

* Sat Aug 27 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 8.3-1
- Update to 8.3

* Sat Aug 13 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 8.2-1
- Update to 8.2

* Thu Apr 28 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 8.1-1
- Update to 8.1

* Mon Feb 22 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 8.0-1
- Update to 8.0

* Wed Jan 20 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 7.3-1
- Update to 7.3

* Wed Jan 6 2016 - Devrim GÜNDÜZ <devrim@gunduz.org> 7.2-1
- Update to 7.2
- Update license
- Use new %%license macro

* Mon Jul 13 2015 - Devrim GÜNDÜZ <devrim@gunduz.org> 7.1-1
- Update to 7.1, per changes described at:
  http://www.postgresql.org/message-id/55A0EB5C.1040900@dalibo.com
- Update download URL.

* Tue May 12 2015 - Devrim GÜNDÜZ <devrim@gunduz.org> 7.0-1
- Update to 7.0
- Minor spec file cosmetic and rpmlint updates.
- Spec file cleanups for RHEL 7 and Fedora 20+.

* Wed Apr 15 2015 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.4-1
- Update to 6.4

* Mon Apr 6 2015 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.3-1
- Update to 6.3
- Fix various rpmlint warnings.

* Thu Oct 16 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.2-1
- Update to 6.2

* Thu Oct 9 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.1-1
- Update to 6.1

* Wed Aug 27 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Tue May 6 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 5.1-1
- Update to 5.1

* Thu Feb 13 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 5.0-1
- Update to 5.0, per changes described at
  http://www.postgresql.org/message-id/2c9e60c9f80fe68276178abe45311d09@dalibo.com

* Fri Nov 08 2013 - Jeff Frost <jeff@pgexperts.com> 4.1-1
- Update to 4.1

* Thu Oct 31 2013 - Jeff Frost <jeff@pgexperts.com> 4.0-1
- Update to 4.0

* Mon Sep 23 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 3.6-1
- Update to 3.6

* Mon Sep 16 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 3.5-1
- Update to 3.5

* Thu Jun 20 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.4-1
- Update to 3.4

* Thu Apr 11 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.2-1
- Update to 3.2

* Tue Feb 26 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Mon Jan 21 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.3-1
- Update to 2.3
- Update download URL.

* Wed Nov 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Thu Nov 1 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Sep 26 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
