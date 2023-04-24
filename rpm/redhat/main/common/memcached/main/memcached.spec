%global username   memcached
%global groupname  memcached
%bcond_without sasl

Name:           memcached
Version:        1.4.39
Release:        1%{?dist}.2
Epoch:          0
Summary:        High Performance, Distributed Memory Object Cache

License:        BSD
URL:            http://www.memcached.org/
Source0:        http://www.memcached.org/files/%{name}-%{version}.tar.gz
Source1:        memcached.sysconfig

Patch1:         memcached-unit.patch

BuildRequires:  libevent-devel
BuildRequires:  perl(Test::More), perl(Test::Harness)
%{?with_sasl:BuildRequires: cyrus-sasl-devel}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%package devel
Summary: Files needed for development using memcached protocol
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.

%prep
%setup -q
%patch -P 1 -p1 -b .unit

%build
# compile with full RELRO
export CFLAGS="%{optflags} -pie -fpie"
export LDFLAGS="-Wl,-z,relro,-z,now"

%configure \
  %{?with_sasl: --enable-sasl}

make %{?_smp_mflags}

%check
# disable testing as it is unreliable on build systems
exit 0

# whitespace tests fail locally on fedpkg systems now that they use git
rm -f t/whitespace.t

# Parts of the test suite only succeed as non-root.
if [ `id -u` -ne 0 ]; then
  # remove failing test that doesn't work in
  # build systems
  rm -f t/daemonize.t t/watcher.t t/expirations.t
fi
make test

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool
install -Dp -m0644 scripts/memcached-tool.1 \
        %{buildroot}%{_mandir}/man1/memcached-tool.1

# Unit file
install -Dp -m0644 scripts/memcached.service \
        %{buildroot}%{_unitdir}/memcached.service

# Default configs
install -Dp -m0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
useradd -r -g %{groupname} -d /run/memcached \
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0


%post
%service_add_post memcached.service


%preun
%service_del_preun memcached.service


%postun
%service_del_postun_with_restart memcached.service


%files
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached-tool.1*
%{_mandir}/man1/memcached.1*
%{_unitdir}/memcached.service


%files devel
%{_includedir}/memcached/*

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0:1.4.39-1.2
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0:1.4.39-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jul 11 2017 Devrim Gündüz <devrim@gunduz.org> - 0:1.4.39-1
- Initial build for PostgreSQL SUSE Repository, based on Fedora
  rawhide package.
