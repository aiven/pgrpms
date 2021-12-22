%global	selinux_variants targeted
%global	selinux_policyver 3.7.19
%global	modulename postgresql-pgdg
%global	relabelpath /usr/pgsql-*/*

Name:		selinux-pgsql-pgdg
Version:	1.5.0
Release:	1%{dist}
Summary:	SELinux policy module for PostgreSQL from the PGDG
License:	PostgreSQL
Url:		http://github.com/dalibo/selinux-pgsql-pgdg
Source0:	https://github.com/dalibo/selinux-pgsql-pgdg/archive/refs/tags/1.5.0.tar.gz

BuildArch:	noarch
BuildRequires:	gcc make
BuildRequires:	selinux-policy-devel

Requires:	selinux-policy >= %{selinux_policyver}
Requires:	selinux-policy-targeted
Requires(post):	/usr/sbin/semodule, /sbin/restorecon
Requires(postun):	/usr/sbin/semodule, /sbin/restorecon

%description
SELinux policy module for PostgreSQL packages provided by the
PGDG. This module adds the file contexts needed to confine a
PostgreSQL cluster.

%prep
%setup -q

%build
for selinuxvariant in %{selinux_variants}
do
	%{__make} NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
	%{__mv} %{modulename}.pp %{modulename}.pp.${selinuxvariant}
	%{__make} NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done

%install
for selinuxvariant in %{selinux_variants}
do
	%{__install} -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	%{__install} -p -m 644 %{modulename}.pp.${selinuxvariant} \
	%{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done

%clean
%{__rm} -rf %{buildroot}

%post
for selinuxvariant in %{selinux_variants}
do
	%{_sbindir}/semodule -s ${selinuxvariant} -u \
	%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done
/sbin/restorecon -R ${relabelpath} || :

%postun
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
	%{_sbindir}/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
  /sbin/restorecon -R %{relabelpath} || :
fi

%files
%defattr(-,root,root,0755)
%{_datadir}/selinux/*/%{modulename}.pp
%doc README.md

%changelog
* Wed Mar 24 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-2
- Minor rpmlint fixes

* Tue Jan 26 2021 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.5.0-1
- Allow to use FUSE filesystems

* Mon Dec 14 2020 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.4.1-1
- Fix restorecon at install and uninstall

* Fri Oct 30 2020 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.4.0-1
- Allow to use NFS

* Mon Sep 21 2020 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.3.1-1
- Fix path of patroni executable

* Sat Sep 19 2020 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 1.3.0-1
- Support Patroni

* Fri Oct 11 2019 Étienne BERSAC <etienne.bersac@dalibo.com> - 1.2.0-1
- Add postgresql_pgdg_can_http boolean.

* Mon Nov 27 2017 Étienne BERSAC <etienne.bersac@dalibo.com> - 1.1.0-2
- Build for noarch
- Add build requires
- Ship README

* Mon Oct 23 2017 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.1.0-1
- support PostgreSQL 10

* Mon Jan 28 2015 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.0.1-1
- Follow the selinux module revision bump for proper rpm update

* Mon Jan 23 2015 Marcus Berglof <marcus.berglof@gmail.com> 1.0.0-2
- Added postgresql_log_t for pgstartup.log and pg_log

* Mon Sep 22 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.0.0-1
- Initial version

