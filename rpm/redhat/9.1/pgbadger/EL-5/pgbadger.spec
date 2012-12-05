Summary:	a fast PostgreSQL log analyzer
Name:		pgbadger
Version:	2.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/downloads/dalibo/pgbadger/%{name}-%{version}-1.tar.gz
URL:		http://dalibo.github.com/pgbadger/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

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

%{__perl} Makefile.PL INSTALLDIRS=vendor

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%perl_vendorarch/auto/pgBadger/.packlist
%{_mandir}/man1/%{name}.1.gz

%changelog
* Wed Nov 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Thu Nov 1 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Thu Sep 26 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
