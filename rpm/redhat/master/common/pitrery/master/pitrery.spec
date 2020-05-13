Name:           pitrery
Version:        3.1
Release:        1%{?dist}
Summary:        Point-In-Time Recovery tools for PostgreSQL
License:        BSD
URL:            https://github.com/dalibo/%{name}
Source0:        https://github.com/dalibo/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch1:         %{name}.config.patch
BuildArch:      noarch
Requires:       bash, rsync

%description
pitrery is set of tools to ease to management of PITR backups and
restores for PostgreSQL.

- Management of WAL segments archiving with compression to hosts
  reachable with SSH
- Automation of the base backup procedure
- Restore to a particular date
- Management of backup retention

%prep
%setup -q
%patch1 -p1

%build
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}  %{?_smp_mflags}

%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/archive_wal
%{_bindir}/archive_xlog
%{_bindir}/%{name}
%{_bindir}/restore_wal
%{_bindir}/restore_xlog
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/COPYRIGHT
%doc %{_docdir}/%{name}/INSTALL.md
%doc %{_docdir}/%{name}/UPGRADE.md
%doc %{_docdir}/%{name}/%{name}.conf
%doc %{_docdir}/%{name}/CHANGELOG
%doc %{_mandir}/man1/%{name}.1.gz
%doc %{_mandir}/man1/archive_wal.1.gz
%doc %{_mandir}/man1/restore_wal.1.gz

%changelog
* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1-1
- Update to 3.1

* Mon Jan 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0-1
- Update to 3.0

* Fri Jul 12 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Update to 2.1

* Tue Mar 6 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0-2
- Minor spec file improvements

* Fri Oct 20 2017 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 2.0-1
* Update to 2.0

* Tue May 23 2017 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.13-1
- Update to 1.13

* Fri Nov 18 2016 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.12-1
- Update to 1.12

* Mon Jun 20 2016 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.11-1
- Update to 1.11

* Mon Oct 19 2015 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.10-1
- Update to 1.10

* Fri Oct  9 2015 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.9-1
- Update to 1.9

* Thu Feb 19 2015 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.8-2
- Do not depend on pax, it is no longer the default

* Wed Dec 31 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.8-1
- Update to 1.8

* Sat Apr 19 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.7-1
- Update to 1.7
- Upstream has removed /usr/bin/pitr_mgr

* Tue Feb 18 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.6-1
- Update to 1.6
- store configuration files in /etc/pitrery

* Sun Sep  1 2013 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.5-1
- Update to 1.5

* Mon Jul 15 2013 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.4-1
- Update to 1.4

* Thu May 30 2013 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.3-1
- Update to 1.3

* Fri Apr  5 2013 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.2-1
- Update to 1.2

* Thu Dec 15 2011 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.1-1
- Update to 1.1

* Thu Aug 11 2011 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.0-1
- Update to 1.0

* Mon Aug  8 2011 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.0rc2-1
- New package

