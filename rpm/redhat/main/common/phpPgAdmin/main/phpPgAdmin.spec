%global		sname phppgadmin

Summary:	Web-based PostgreSQL administration
Name:		phpPgAdmin
Version:	7.13.0
Release:	1%{?dist}.1
License:	GPLv2+ and (LGPLv2+ or BSD) and ASL 2.0 and MIT
URL:		https://github.com/%{sname}/%{sname}

Source0:	https://github.com/%{sname}/%{sname}/releases/download/REL_7-13-0/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf

Requires:	php >= 7.2, gawk
Requires:	php-pgsql >= 7.2, httpd
Requires(post):	systemd
Requires(postun):	systemd
BuildArch:	noarch

%global		_phppgadmindir	%{_datadir}/%{name}

Patch1:		%{name}-langcheck.patch

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procedures). It also has Slony-I support.

%prep
%setup -q -n %{name}-%{version}
%patch -P 1 -p0

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_phppgadmindir}
%{__install} -d %{buildroot}%{_phppgadmindir}/conf
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__install} -m 644 -p *.php %{buildroot}%{_phppgadmindir}
%{__cp} -ap *.js robots.txt classes help js libraries themes images lang plugins xloadtree %{buildroot}%{_phppgadmindir}
%{__install} -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}
%{__ln_s} %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_phppgadmindir}/conf/config.inc.php
%{__ln_s} %{_sysconfdir}/%{name}/config.inc.php-dist %{buildroot}/%{_phppgadmindir}/conf/config.inc.php-dist

%post
/usr/bin/systemctl reload httpd.service

%postun
/usr/bin/systemctl reload httpd.service

%files
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL LICENSE TODO TRANSLATORS
%dir %{_phppgadmindir}
%dir %{_sysconfdir}/%{name}
%dir %{_phppgadmindir}/conf
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(644,root,root) %{_phppgadmindir}/*.php
%{_phppgadmindir}/*.js
%{_phppgadmindir}/robots.txt
%{_phppgadmindir}/classes
%{_phppgadmindir}/help
%{_phppgadmindir}/images
%{_phppgadmindir}/js/*.js
%{_phppgadmindir}/libraries
%{_phppgadmindir}/plugins/Report/*
%{_phppgadmindir}/plugins/GuiControl/*
%{_phppgadmindir}/themes
%{_phppgadmindir}/xloadtree
%{_phppgadmindir}/conf/*
%dir %{_phppgadmindir}/lang
%attr(644,root,root) %{_phppgadmindir}/lang/*.php
%attr(644,root,root) %{_phppgadmindir}/lang/README
%attr(755,root,root) %{_phppgadmindir}/lang/langcheck
%attr(755,root,root) %{_phppgadmindir}/lang/synch

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 7.13.0-1.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Nov 9 2020 Devrim Gündüz <devrim@gunduz.org> - 7.13.0-1
- Update to 7.13.0

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 7.12.1-1
- Update to 7.12.1

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 5.6-1
- Update to 5.6
- Fix a few rpmlint warnings
- Update URLs
- Use more macros
