%define haproxy_user	haproxy
%define haproxy_group	%{haproxy_user}
%define haproxy_homedir	%{_localstatedir}/lib/haproxy
%define haproxy_confdir	%{_sysconfdir}/haproxy
%define haproxy_datadir	%{_datadir}/haproxy

%global _hardened_build 1

Name:		haproxy
Version:	2.8.3
Release:	1PGDG%{?dist}
Summary:	HAProxy reverse proxy for high availability environments

License:	GPLv2+

URL:		https://www.haproxy.org/
Source0:	https://www.haproxy.org/download/2.8/src/%{name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.cfg
Source3:	%{name}.logrotate
Source4:	%{name}.sysconfig
Source5:	halog.1

BuildRequires:	gcc lua-devel pcre2-devel make
BuildRequires:	openssl-devel systemd-devel systemd

Requires(pre):	shadow-utils
%{?systemd_requires}

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence
   through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI
   intercepted from the application

%prep
%setup -q

%build
regparm_opts=
%ifarch %ix86 x86_64
regparm_opts="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_SLZ=1 USE_LUA=1 USE_CRYPT_H=1 USE_SYSTEMD=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 USE_PROMEX=1 DEFINE=-DMAX_SESS_STKCTR=12 ${regparm_opts} ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}"

%{__make} admin/halog/halog ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}"

pushd admin/iprange
%{__make} OPTIMIZE="%{build_cflags}" LDFLAGS="%{build_ldflags}"
popd

%install
%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} TARGET="linux2628"
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/halog.1
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 ./admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range

for httpfile in $(find ./examples/errorfiles/ -type f)
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

%{__rm} -rf ./examples/errorfiles/

find ./examples/* -type f ! -name "*.cfg" -exec %{__rm} -f "{}" \;

for textfile in $(find ./ -type f -name '*.txt')
do
    %{__mv} $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    %{__rm} -f $textfile.old
done

%pre
getent group %{haproxy_group} >/dev/null || \
    groupadd -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || \
    useradd -r -g %{haproxy_user} -d %{haproxy_homedir} \
    -s /sbin/nologin -c "haproxy" %{haproxy_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc doc/* examples/*
%doc CHANGELOG README VERSION
%license LICENSE
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/*

%changelog
* Fri Sep 8 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.3-1PGDG
- Update to 2.8.3

* Wed Aug 9 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.2-1PGDG
- Update to 2.8.2
- Add PGDG branding

* Mon Jul 3 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.1-1
- Update to 2.8.1

* Fri Jun 2 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.0-1
- Update to 2.8.0

* Thu May 4 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.8-1
- Update to 2.7.8

* Mon Apr 10 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.6-1
- Update to 2.7.6

* Tue Mar 21 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.5-1
- Update to 2.7.5

* Sun Mar 12 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.4-1
- Update to 2.7.4

* Wed Feb 15 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Mon Jan 30 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.2-1
- Update to 2.7.2

* Tue Dec 20 2022 - Devrim Gündüz <devrim@gunduz.org> 2.7.1-1
- Update to 2.7.1

* Thu Dec 15 2022 - Devrim Gündüz <devrim@gunduz.org> 2.7.0-1
- Update to 2.7.0

* Thu Dec 15 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.7-1
- Update to 2.6.7

* Fri Sep 23 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.6-1
- Update to 2.6.6

* Fri Sep 9 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.5-1
- Update to 2.6.5

* Mon Aug 22 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.3-1
- Update to 2.6.3

* Wed Jul 27 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2

* Tue May 31 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.7-1
- Update to 2.5.7

* Wed May 11 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.6-1
- Update to 2.5.6

* Wed Apr 20 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.5-1
- Update to 2.5.5

* Mon Mar 14 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.4-1
- Initial RPM packaging for the PostgreSQL RPM Repository
