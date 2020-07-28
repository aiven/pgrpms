Name:		pgagroal
Version:	0.7.3
Release:	1%{dist}
Summary:	High-performance connection pool for PostgreSQL
License:	BSD
URL:		https://github.com/agroal/pgagroal
Source0:	https://github.com/agroal/pgagroal/archive/%{version}.tar.gz

BuildRequires:	gcc cmake make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel chrpath
Requires:	libev openssl

%description
pgagroal is a high-performance connection pool for PostgreSQL.

%prep
%setup -q

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
%{__make}

%install

%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{_libdir}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/images
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__mkdir} -p %{buildroot}%{_mandir}/man5
%{__mkdir} -p %{buildroot}%{_sysconfdir}/pgagroal

%{__install} -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
%{__install} -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/ARCHITECTURE.md %{buildroot}%{_docdir}/%{name}/ARCHITECTURE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/CONFIGURATION.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/GETTING_STARTED.md %{buildroot}%{_docdir}/%{name}/GETTING_STARTED.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/PERFORMANCE.md %{buildroot}%{_docdir}/%{name}/PERFORMANCE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/RPM.md %{buildroot}%{_docdir}/%{name}/RPM.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-extended.png %{buildroot}%{_docdir}/%{name}/images/perf-extended.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-prepared.png %{buildroot}%{_docdir}/%{name}/images/perf-prepared.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-readonly.png %{buildroot}%{_docdir}/%{name}/images/perf-readonly.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-simple.png %{buildroot}%{_docdir}/%{name}/images/perf-simple.png

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/pgagroal.conf %{buildroot}%{_sysconfdir}/pgagroal/pgagroal.conf
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/pgagroal_hba.conf %{buildroot}%{_sysconfdir}/pgagroal/pgagroal_hba.conf

%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal.1 %{buildroot}%{_mandir}/man1/pgagroal.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal-admin.1 %{buildroot}%{_mandir}/man1/pgagroal-admin.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal-cli.1 %{buildroot}%{_mandir}/man1/pgagroal-cli.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal.conf.5 %{buildroot}%{_mandir}/man5/pgagroal.conf.5
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal_databases.conf.5 %{buildroot}%{_mandir}/man5/pgagroal_databases.conf.5
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/pgagroal_hba.conf.5 %{buildroot}%{_mandir}/man5/pgagroal_hba.conf.5

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/pgagroal %{buildroot}%{_bindir}/pgagroal
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/pgagroal-cli %{buildroot}%{_bindir}/pgagroal-cli
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/pgagroal-admin %{buildroot}%{_bindir}/pgagroal-admin

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/libpgagroal.so.%{version} %{buildroot}%{_libdir}/libpgagroal.so.%{version}

chrpath -r %{_libdir} %{buildroot}%{_bindir}/pgagroal
chrpath -r %{_libdir} %{buildroot}%{_bindir}/pgagroal-cli
chrpath -r %{_libdir} %{buildroot}%{_bindir}/pgagroal-admin

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgagroal.so.%{version} libpgagroal.so.0
%{__ln_s} -f libpgagroal.so.0 libpgagroal.so

%files
%license %{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/ARCHITECTURE.md
%{_docdir}/%{name}/CONFIGURATION.md
%{_docdir}/%{name}/GETTING_STARTED.md
%{_docdir}/%{name}/PERFORMANCE.md
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/RPM.md
%{_docdir}/%{name}/images/perf-extended.png
%{_docdir}/%{name}/images/perf-prepared.png
%{_docdir}/%{name}/images/perf-readonly.png
%{_docdir}/%{name}/images/perf-simple.png
%{_mandir}/man1/pgagroal.1*
%{_mandir}/man1/pgagroal-admin.1*
%{_mandir}/man1/pgagroal-cli.1*
%{_mandir}/man5/pgagroal.conf.5*
%{_mandir}/man5/pgagroal_databases.conf.5*
%{_mandir}/man5/pgagroal_hba.conf.5*
%config %{_sysconfdir}/pgagroal/pgagroal.conf
%config %{_sysconfdir}/pgagroal/pgagroal_hba.conf
%{_bindir}/pgagroal
%{_bindir}/pgagroal-cli
%{_bindir}/pgagroal-admin
%{_libdir}/libpgagroal.so
%{_libdir}/libpgagroal.so.0
%{_libdir}/libpgagroal.so.%{version}

%changelog
* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.3-1
- Update to 0.7.3

* Wed Jun 10 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1
- Update to 0.7.1

* Wed May 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0

* Fri May 1 2020 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Update to 0.6.0

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1
- Update to 0.5.1

* Tue Mar 24 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
