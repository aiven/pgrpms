%global sname	pgmoneta

Name:		%{sname}
Version:	0.4.0
Release:	1%{dist}
Summary:	Backup / restore for PostgreSQL
License:	BSD
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/%{sname}/%{sname}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake make python3-docutils zlib-devel libzstd-devel
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
Requires:	libev openssl systemd postgresql zlib libzstd

Obsoletes:	%{sname}_13 < 0.2.0-2

%description
pgmoneta is a backup / restore solution for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_INSTALL_PREFIX=/usr
%{__make}

%install
cd build
%{__make} install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{sname}
%{__mv} %{buildroot}/usr/etc/%{sname}/%{sname}.conf %{buildroot}%{_sysconfdir}/%{sname}

%files
%license LICENSE
%{_bindir}/%{sname}
%{_bindir}/%{sname}-admin
%{_bindir}/%{sname}-cli
%config %{_sysconfdir}/%{sname}/%{sname}.conf
%{_libdir}/libpgmoneta.so*
%dir %{_docdir}/%{sname}
%{_docdir}/%{sname}/*
%{_mandir}/man1/%{sname}*
%{_mandir}/man5/%{sname}*

%changelog
* Thu Aug 12 2021 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Tue Jul 20 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Sun Jul 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0

* Thu Jun 17 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-2
- Remove PostgreSQL version number from the package. This
  is a common one.

* Mon Jun 14 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Update to 0.2.0

* Fri May 28 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Took spec
  file from upstream.
